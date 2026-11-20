import threading

from generator.cli import run
from generator.config import ClickHouseSettings, GeneratorSettings, Settings


class RecordingSink:
    def __init__(self, stop, start_id=100):
        self.stop = stop
        self.start_id = start_id
        self.batches = []
        self.heroes = []
        self.players = []
        self.closed = False

    def setup(self, heroes, players):
        self.heroes, self.players = list(heroes), list(players)

    def next_match_id(self):
        return self.start_id

    def write_facts(self, facts):
        self.batches.append(list(facts))
        self.stop.set()  # одного батча достаточно

    def close(self):
        self.closed = True


def make_settings(**overrides):
    generator = GeneratorSettings(
        _env_file=None, batch_size=5, interval_seconds=0.0, players_count=10, **overrides
    )
    return Settings(generator=generator, clickhouse=ClickHouseSettings(_env_file=None))


def test_run_writes_one_batch_and_closes_sink():
    stop = threading.Event()
    sink = RecordingSink(stop)
    run(make_settings(), stop, sink)

    assert len(sink.batches) == 1
    assert [f.match_id for f in sink.batches[0]] == [100, 101, 102, 103, 104]
    assert len(sink.players) == 10
    assert sink.closed


def test_run_does_nothing_if_already_stopped():
    stop = threading.Event()
    stop.set()
    sink = RecordingSink(stop)
    run(make_settings(), stop, sink)

    assert sink.batches == []
    assert sink.closed
