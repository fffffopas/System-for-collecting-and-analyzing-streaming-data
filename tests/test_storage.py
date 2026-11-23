from datetime import UTC, datetime, timedelta

import pytest

from generator.models import Hero, Player, TableFacts
from generator.retry import RetryError, RetryPolicy
from generator.storage import (
    DDL_MATCH_FACTS,
    FACT_COLUMNS,
    ClickHouseSink,
    LogSink,
    fact_to_row,
)

NOW = datetime(2026, 11, 15, 12, 0, tzinfo=UTC)


class FakeClient:
    def __init__(self, fail_times=0, max_match_id=0):
        self.calls = []
        self.fail_times = fail_times
        self.max_match_id = max_match_id
        self.disconnected = False

    def execute(self, query, params=None):
        if self.fail_times > 0:
            self.fail_times -= 1
            raise ConnectionError("clickhouse is down")
        self.calls.append((" ".join(query.split()), params))
        if query.startswith("SELECT max(match_id)"):
            return [(self.max_match_id,)]
        return []

    def disconnect(self):
        self.disconnected = True


def make_fact(match_id=1):
    return TableFacts(
        match_id=match_id,
        event_time=NOW,
        player_id=3,
        hero_id=5,
        side="radiant",
        role="carry",
        match_time=timedelta(minutes=41, seconds=30),
        result=True,
        mmr_delta=27,
        gpm=612.5,
        xpm=640.0,
        kills=10,
        deaths=2,
        assists=7,
        rampage=False,
        abandoned=True,
        report_received=False,
        commend_received=False,
        entered_low_priority=False,
    )


def make_sink(client):
    retry = RetryPolicy(3, 0.1, 1.0, jitter=0.0, sleep=lambda s: None)
    return ClickHouseSink(client, retry)


def test_fact_row_matches_columns():
    row = fact_to_row(make_fact())
    assert len(row) == len(FACT_COLUMNS)
    values = dict(zip(FACT_COLUMNS, row, strict=True))
    assert values["match_duration_sec"] == 41 * 60 + 30
    assert values["result"] == 1
    assert values["abandoned"] == 1
    assert values["rampage"] == 0
    assert values["event_time"] == NOW


def test_every_fact_column_is_in_ddl():
    for column in FACT_COLUMNS:
        assert f"    {column} " in DDL_MATCH_FACTS


def test_setup_creates_tables_and_inserts_dimensions():
    client = FakeClient()
    sink = make_sink(client)
    players = [Player(1, 3000, "p1", "DE", "EU", NOW)]
    sink.setup([Hero(1, "Axe")], players)

    queries = [q for q, _ in client.calls]
    assert sum(q.startswith("CREATE TABLE") for q in queries) == 3
    assert any(q.startswith("INSERT INTO heroes") for q in queries)
    assert any(q.startswith("INSERT INTO players") for q in queries)


def test_write_facts_inserts_rows():
    client = FakeClient()
    make_sink(client).write_facts([make_fact(1), make_fact(2)])

    query, rows = client.calls[-1]
    assert query.startswith("INSERT INTO match_facts (match_id, event_time")
    assert [r[0] for r in rows] == [1, 2]


def test_write_empty_batch_does_nothing():
    client = FakeClient()
    make_sink(client).write_facts([])
    assert client.calls == []


def test_next_match_id_continues_after_max():
    assert make_sink(FakeClient(max_match_id=0)).next_match_id() == 1
    assert make_sink(FakeClient(max_match_id=41)).next_match_id() == 42


def test_retries_on_connection_error():
    client = FakeClient(fail_times=2)
    make_sink(client).write_facts([make_fact()])
    assert len(client.calls) == 1


def test_gives_up_after_max_attempts():
    client = FakeClient(fail_times=10)
    with pytest.raises(RetryError):
        make_sink(client).write_facts([make_fact()])


def test_close_disconnects():
    client = FakeClient()
    make_sink(client).close()
    assert client.disconnected


def test_log_sink_is_noop():
    sink = LogSink()
    sink.setup([], [])
    assert sink.next_match_id() == 1
    sink.write_facts([make_fact()])
    sink.close()
