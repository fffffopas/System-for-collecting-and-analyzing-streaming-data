from __future__ import annotations

import random
from datetime import datetime

from generator.models import Player, Hero, TableFacts

from .anomaly import AnomalyKind, AnomalyPolicy
from .metrics import (
    DotaProfile,
    MmrBeforeSample,
    MmrDeltaSample,
    ResultsSample,
    KillsSample,
    DeathsSample,
    AssistsSample,
    GpmSampler,
    XpmSampler,
    MatchTimeSampler,
    MatchContext,
    MetricSampler
)

class MathcGenereator:
    def __init__(
        self, 
        profile: DotaProfile,
        anomaly_policy: AnomalyPolicy,
        rng: random.Random
    ) -> None:

        self._profile = profile
        self._rng = rng
        self._anomaly_policy = anomaly_policy

        self._mmr_before: MetricSampler = MmrBefore(profile)
        self._result: MetricSampler = Results(profile)
        self._kills: MetricSampler = Kills(profile)
        self._deaths: MetricSampler = Deaths(profile)
        self._assists: MetricSampler = Assists(profile)
        self._mmr_delta: MetricSampler = MmrDelta(profile)
        self._gpm: MetricSampler = GpmSampler(profile)
        self._xpm: MetricSampler = XpmSampler(profile)
        self._match_time: MetricSampler = MatchTimeSampler(profile)

        self._next_match_id = 1

    def generator(self, player: Player, hero: Hero, at: datetime) -> TableFacts:
        
        rng = self._rng
        anomaly = self._anomaly_policy.decide(self._rng)

        ctx = MatchContext(at=at, player=Player, hero = Hero)
        mmr_before = self._mmr_before.sample(ctx, rng)

        ctx = MatchContext(at = at, player=Player, hero=Hero, mmr_before=mmr_before)
        result = self._apply_result_anomaly(self._result.sample(ctx, rng))
 
        ctx = MatchContext(at=at, player=Player, hero=Hero, mmr_before=mmr_before, result=result)
        kills = self._kills.sample(ctx, rng)
        deaths = self._deaths.sample(ctx, rng)
        assists = self._assists.sample(ctx, rng)
        gpm = self._gpm.sample(ctx, rng)
        xpm = self._xpm.sample(ctx, rng)
        match_time = self._match_time.sample(ctx, rng)

        ctx = MatchContext(
            at=at, player=player, hero=hero,
            mmr_before=mmr_before, result=result,
            kills=kills, deaths=deaths, assists=assists,
            anomaly=anomaly,
        )
        mmr_delta = self._mmr_delta.sample(ctx, rng)

        match_id = self._next_match_id
        self._next_match_id += 1

        return TableFacts(
            match_id=match_id,
            player_id=player.player_id,
            hero_id=hero.hero_id,
            match_time=match_time,
            result=result,
            mmr_before=mmr_before,
            mmr_delta=mmr_delta,
            gpm=gpm,
            xpm=xpm,
            kills=kills,
            deaths=deaths,
            assists=assists,
            rampage=False,          # TODO: BernoulliSampler
            report_received=False,  # TODO
            commend_received=False, # TODO
            entered_low_priority=False,  # TODO
        )



        