import random

from generator.generation import defaults
from generator.generation.metrics import DotaProfile
from generator.generation.population import make_heroes, make_players, pick_country


def test_heroes_have_unique_sequential_ids():
    heroes = make_heroes()
    assert [h.hero_id for h in heroes] == list(range(1, len(heroes) + 1))
    assert len({h.hero_name for h in heroes}) == len(heroes)


def test_players_are_deterministic_for_seed():
    a = make_players(50, DotaProfile(), random.Random(1))
    b = make_players(50, DotaProfile(), random.Random(1))
    assert a == b


def test_players_fields_are_valid():
    players = make_players(200, DotaProfile(), random.Random(7))
    assert len(players) == 200
    for p in players:
        assert defaults.MMR_MIN <= p.mmr <= defaults.MMR_MAX
        assert p.country in defaults.COUNTRY_WEIGHTS_BY_REGION[p.region]
        assert p.registered_at.tzinfo is not None


def test_unknown_region_gets_default_country():
    assert pick_country("MARS", random.Random(1)) == defaults.DEFAULT_COUNTRY
