"""Куда уходят сгенерированные данные: ClickHouse или просто в лог (dry-run)."""

from __future__ import annotations

import logging
from collections.abc import Sequence
from typing import TYPE_CHECKING, Any, Protocol

from generator.models import Hero, Player, TableFacts
from generator.retry import RetryPolicy

if TYPE_CHECKING:
    from generator.config import ClickHouseSettings

logger = logging.getLogger(__name__)

# --- Схема -------------------------------------------------------------------
# Измерения (heroes, players) - ReplacingMergeTree: при каждом старте генератор
# записывает их заново, дубликаты схлопываются при слиянии кусков
# (в запросах используйте FINAL, если нужна гарантия уникальности).
# Факты (match_facts) - MergeTree, партиции по месяцам.

DDL_HEROES = """
CREATE TABLE IF NOT EXISTS heroes (
    hero_id UInt16,
    hero_name String
) ENGINE = ReplacingMergeTree
ORDER BY hero_id
"""

DDL_PLAYERS = """
CREATE TABLE IF NOT EXISTS players (
    player_id UInt32,
    nickname String,
    country LowCardinality(String),
    region LowCardinality(String),
    mmr UInt32,
    registered_at DateTime('UTC'),
    updated_at DateTime('UTC') DEFAULT now()
) ENGINE = ReplacingMergeTree(updated_at)
ORDER BY player_id
"""

DDL_MATCH_FACTS = """
CREATE TABLE IF NOT EXISTS match_facts (
    match_id UInt64,
    event_time DateTime('UTC'),
    player_id UInt32,
    hero_id UInt16,
    side LowCardinality(String),
    role LowCardinality(String),
    match_duration_sec UInt32,
    result UInt8,
    mmr_delta Int16,
    gpm Float32,
    xpm Float32,
    kills UInt16,
    deaths UInt16,
    assists UInt16,
    rampage UInt8,
    abandoned UInt8,
    report_received UInt8,
    commend_received UInt8,
    entered_low_priority UInt8
) ENGINE = MergeTree
PARTITION BY toYYYYMM(event_time)
ORDER BY (event_time, player_id, match_id)
"""

HERO_COLUMNS = ("hero_id", "hero_name")
PLAYER_COLUMNS = (
    "player_id",
    "nickname",
    "country",
    "region",
    "mmr",
    "registered_at",
)
FACT_COLUMNS = (
    "match_id",
    "event_time",
    "player_id",
    "hero_id",
    "side",
    "role",
    "match_duration_sec",
    "result",
    "mmr_delta",
    "gpm",
    "xpm",
    "kills",
    "deaths",
    "assists",
    "rampage",
    "abandoned",
    "report_received",
    "commend_received",
    "entered_low_priority",
)


def hero_to_row(hero: Hero) -> tuple:
    return (hero.hero_id, hero.hero_name)


def player_to_row(player: Player) -> tuple:
    return (
        player.player_id,
        player.nickname,
        player.country,
        player.region,
        player.mmr,
        player.registered_at,
    )


def fact_to_row(fact: TableFacts) -> tuple:
    """Порядок значений строго соответствует FACT_COLUMNS."""
    return (
        fact.match_id,
        fact.event_time,
        fact.player_id,
        fact.hero_id,
        fact.side,
        fact.role,
        int(fact.match_time.total_seconds()),
        int(fact.result),
        fact.mmr_delta,
        fact.gpm,
        fact.xpm,
        fact.kills,
        fact.deaths,
        fact.assists,
        int(fact.rampage),
        int(fact.abandoned),
        int(fact.report_received),
        int(fact.commend_received),
        int(fact.entered_low_priority),
    )


class Sink(Protocol):
    """Интерфейс приёмника данных (ClickHouse, dry-run, тестовая заглушка)."""

    def setup(self, heroes: Sequence[Hero], players: Sequence[Player]) -> None:
        """Подготовить хранилище и записать справочники."""

    def next_match_id(self) -> int:
        """С какого match_id продолжать нумерацию."""

    def write_facts(self, facts: Sequence[TableFacts]) -> None:
        """Записать батч фактов."""

    def close(self) -> None:
        """Освободить ресурсы."""


class LogSink:
    """Режим dry-run: ничего никуда не пишет, только логирует."""

    def setup(self, heroes: Sequence[Hero], players: Sequence[Player]) -> None:
        logger.info(
            "dry-run: %d героев и %d игроков (запись в БД отключена)",
            len(heroes),
            len(players),
        )

    def next_match_id(self) -> int:
        return 1

    def write_facts(self, facts: Sequence[TableFacts]) -> None:
        logger.debug("dry-run: пример строки: %s", facts[0] if facts else None)

    def close(self) -> None:
        pass


class ClickHouseSink:
    """Запись в ClickHouse. Каждое обращение к БД обёрнуто в RetryPolicy."""

    def __init__(self, client: Any, retry: RetryPolicy) -> None:
        self._client = client
        self._retry = retry

    @classmethod
    def from_settings(
        cls, settings: ClickHouseSettings, retry: RetryPolicy
    ) -> ClickHouseSink:
        # Импорт здесь, чтобы dry-run и тесты не требовали установленного драйвера.
        from clickhouse_driver import Client

        client = Client(
            host=settings.host,
            port=settings.port,
            user=settings.user or "default",
            password=settings.password,
            database=settings.database,
        )
        return cls(client, retry)

    def _execute(self, query: str, params: Any = None) -> Any:
        return self._retry.execute(lambda: self._client.execute(query, params))

    def setup(self, heroes: Sequence[Hero], players: Sequence[Player]) -> None:
        for ddl in (DDL_HEROES, DDL_PLAYERS, DDL_MATCH_FACTS):
            self._execute(ddl)
        self._insert("heroes", HERO_COLUMNS, [hero_to_row(h) for h in heroes])
        self._insert("players", PLAYER_COLUMNS, [player_to_row(p) for p in players])
        logger.info(
            "ClickHouse готов: схема создана, записано %d героев и %d игроков",
            len(heroes),
            len(players),
        )

    def next_match_id(self) -> int:
        """Продолжаем нумерацию с места остановки, чтобы match_id не повторялись."""
        rows = self._execute("SELECT max(match_id) FROM match_facts")
        return int(rows[0][0]) + 1

    def write_facts(self, facts: Sequence[TableFacts]) -> None:
        if facts:
            self._insert("match_facts", FACT_COLUMNS, [fact_to_row(f) for f in facts])

    def _insert(self, table: str, columns: Sequence[str], rows: list[tuple]) -> None:
        query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES"
        self._execute(query, rows)

    def close(self) -> None:
        self._client.disconnect()
