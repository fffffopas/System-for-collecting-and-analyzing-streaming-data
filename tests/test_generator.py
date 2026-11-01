import random
from datetime import datetime

from generator.generation.anomaly import AnomalyPolicy
from generator.generation.match_generator import MatchGenerator
from generator.generation.metrics import DotaProfile
from generator.models import Hero, Player


def make_gen(seed=42):
    return MatchGenerator(DotaProfile(), AnomalyPolicy(0.02, 1.0), random.Random(seed))


def make_player():
    return Player(1, 3000, "p1", "DE", "EU", datetime(2024, 1, 1))


HERO = Hero(1, "Anti-Mage")
NOW = datetime(2025, 1, 1)


def test_same_seed_same_data():
    a = [make_gen().generate(make_player(), HERO, NOW) for _ in range(1)]
    b = [make_gen().generate(make_player(), HERO, NOW) for _ in range(1)]
    assert a == b


def test_values_are_sane():
    gen = make_gen()
    for _ in range(500):
        f = gen.generate(make_player(), HERO, NOW)
        assert f.kills >= 0 and f.deaths >= 0 and f.assists >= 0
        assert 50 <= f.gpm <= 1500
        assert f.side in ("radiant", "dire")


def test_match_ids_increment():
    gen = make_gen()
    p = make_player()
    ids = [gen.generate(p, HERO, NOW).match_id for _ in range(5)]
    assert ids == [1, 2, 3, 4, 5]


def test_mmr_changes_after_match():
    gen = make_gen()
    p = make_player()
    before = p.mmr
    f = gen.generate(p, HERO, NOW)
    assert p.mmr == max(0, before + f.mmr_delta)