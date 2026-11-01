from __future__ import annotations

import random
import time

from datetime import datetime, timedelta, timezone
from generator.config import get_settings 
from generator.models import Player, Hero, TableFacts
from generator.generation.metrics import DotaProfile, _clamp
from generator.generation.anomaly import AnomalyPolicy
from generator.generation.match_generator import MatchGenerator
from generator.generation import defaults


COUNTRY_BY_REGION = {"EU": "DE", "NA": "US", "SEA": "SG", "CN": "CN", "SA": "BR", "CIS": "KZ"}
PLAYERS_COUNT = 500

def make_heroes() -> list[Hero]:
    return [Hero(hero_id=i, hero_name=name)
            for i, name in enumerate(defaults.ALL_HEROES, start=1)]

def make_players(n: int, profile: DotaProfile, rng: random.Random) -> list[Player]:
    players = []
    regions = list(profile.region_mmr_mean)

    for i in range(1, n + 1):
        region = rng.choice(regions)
        mmr = int(_clamp(rng.gauss(profile.region_mmr_mean[region], profile.mmr_noise_std), 0, 14000))
        players.append(Player(
            player_id=i,
            mmr=mmr,
            nickname=f"player_{i}",
            country=COUNTRY_BY_REGION.get(region, "XX"), region=region,
            registered_at=datetime(2024, 1, 1) + timedelta(days=rng.randint(0, 600))
            
        ))
    return players

def main():
    settings = get_settings()
    cfg = settings.generator
    rng = random.Random(cfg.seed)

    profile = DotaProfile()
    policy = AnomalyPolicy(cfg.anomaly_probability, cfg.anomaly_strength)
    generator = MatchGenerator(profile, policy, rng)

    heroes = make_heroes()
    players = make_players(PLAYERS_COUNT, profile, rng)

    try:
        while True:
            now = datetime.now(timezone.utc)
            batch = [generator.generate(rng.choice(players), rng.choice(heroes), now) for _ in range(cfg.batch_size)]
            # Запись в ClickHouse
            print(batch)
            time.sleep(cfg.interval_seconds)
    except KeyboardInterrupt:
        print("Stopped by user")

if __name__ == "__main__":
    main()