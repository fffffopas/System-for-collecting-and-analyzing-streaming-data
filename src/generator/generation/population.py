from __future__ import annotations

import random
from datetime import UTC, datetime, timedelta

from generator.generation import defaults
from generator.generation.metrics import DotaProfile, clamp
from generator.models import Hero, Player

REGISTRATION_START = datetime(2024, 1, 1, tzinfo=UTC)
REGISTRATION_SPAN_DAYS = 600


def make_heroes() -> list[Hero]:
    return [
        Hero(hero_id=i, hero_name=name)
        for i, name in enumerate(defaults.ALL_HEROES, start=1)
    ]


def pick_country(region: str, rng: random.Random) -> str:
    weights = defaults.COUNTRY_WEIGHTS_BY_REGION.get(region)
    if not weights:
        return defaults.DEFAULT_COUNTRY
    return rng.choices(list(weights), weights=list(weights.values()), k=1)[0]


def make_players(n: int, profile: DotaProfile, rng: random.Random) -> list[Player]:
    regions = list(profile.region_mmr_mean)
    players = []

    for player_id in range(1, n + 1):
        region = rng.choice(regions)
        mmr = int(
            clamp(
                rng.gauss(profile.region_mmr_mean[region], profile.mmr_noise_std),
                defaults.MMR_MIN,
                defaults.MMR_MAX,
            )
        )
        players.append(
            Player(
                player_id=player_id,
                mmr=mmr,
                nickname=f"player_{player_id}",
                country=pick_country(region, rng),
                region=region,
                registered_at=REGISTRATION_START
                + timedelta(days=rng.randint(0, REGISTRATION_SPAN_DAYS)),
            )
        )
    return players
