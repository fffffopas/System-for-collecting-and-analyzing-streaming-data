from __future__ import annotations

import logging
import random
import signal
import threading
from datetime import UTC, datetime

from generator.config import Settings, get_settings
from generator.generation.anomaly import AnomalyPolicy
from generator.generation.match_generator import MatchGenerator
from generator.generation.metrics import DotaProfile
from generator.generation.population import make_heroes, make_players
from generator.logging_setup import setup_logging
from generator.retry import RetryError, RetryPolicy
from generator.storage import ClickHouseSink, LogSink, Sink

logger = logging.getLogger(__name__)


def build_retry(settings: Settings) -> RetryPolicy:
    cfg = settings.generator
    return RetryPolicy(
        max_attempts=cfg.retry_max_attempts,
        base_delay=cfg.retry_base_delay,
        max_delay=cfg.retry_max_delay,
        backoff_factor=cfg.retry_backoff_factor,
    )


def build_sink(settings: Settings, retry: RetryPolicy) -> Sink:
    if settings.generator.dry_run:
        return LogSink()
    return ClickHouseSink.from_settings(settings.clickhouse, retry)


def run(settings: Settings, stop: threading.Event, sink: Sink | None = None) -> None:
    """Основной цикл: генерируем батч -> пишем в sink -> ждём interval."""
    cfg = settings.generator
    rng = random.Random(cfg.seed)

    profile = DotaProfile()
    policy = AnomalyPolicy(cfg.anomaly_probability, cfg.anomaly_strength)

    heroes = make_heroes()
    players = make_players(cfg.players_count, profile, rng)
    sink = sink or build_sink(settings, build_retry(settings))

    try:
        sink.setup(heroes, players)
        generator = MatchGenerator(
            profile, policy, rng, start_match_id=sink.next_match_id()
        )
        logger.info(
            "Старт: batch_size=%d, interval=%.1fs, seed=%d, dry_run=%s",
            cfg.batch_size,
            cfg.interval_seconds,
            cfg.seed,
            cfg.dry_run,
        )
        while not stop.is_set():
            now = datetime.now(UTC)
            batch = [
                generator.generate(rng.choice(players), rng.choice(heroes), now)
                for _ in range(cfg.batch_size)
            ]
            sink.write_facts(batch)
            logger.info(
                "Записан батч: %d матчей (match_id %d..%d)",
                len(batch),
                batch[0].match_id,
                batch[-1].match_id,
            )
            stop.wait(cfg.interval_seconds)
    finally:
        sink.close()


def main() -> int:
    settings = get_settings()
    setup_logging(settings.generator.log_level)

    stop = threading.Event()
    for sig in (signal.SIGINT, signal.SIGTERM):
        signal.signal(sig, lambda *_: stop.set())

    try:
        run(settings, stop)
    except RetryError:
        logger.exception("Не удалось выполнить операцию после всех повторов")
        return 1
    logger.info("Остановлено пользователем")
    return 0
