from __future__ import annotations

import random
from datetime import datetime
from dataclasses import replace

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

        self._mmr_before: MetricSampler = MmrBeforeSample(profile)
        self._result: MetricSampler = ResultsSample(profile)
        self._kills: MetricSampler = KillsSample(profile)
        self._deaths: MetricSampler = DeathsSample(profile)
        self._assists: MetricSampler = AssistsSample(profile)
        self._mmr_delta: MetricSampler = MmrDeltaSample(profile)
        self._gpm: MetricSampler = GpmSampler(profile)
        self._xpm: MetricSampler = XpmSampler(profile)
        self._match_time: MetricSampler = MatchTimeSampler(profile)

        self._next_match_id = 1

    def generator(self, player: Player, hero: Hero, at: datetime) -> TableFacts:
        
        rng = self._rng
        anomaly = self._anomaly_policy.decide(self._rng)

        ctx = MatchContext(at=at, player=player, hero=hero)
        
        ctx.mmr_before = self._mmr_before.sample(ctx, rng)
        ctx.result     = self._result.sample(ctx, rng)
        ctx.kills      = self._kills.sample(ctx, rng)
        ctx.deaths     = self._deaths.sample(ctx, rng)
        ctx.assists    = self._assists.sample(ctx, rng)
        ctx.mmr_delta  = self._mmr_delta.sample(ctx, rng)
        ctx.gpm        = self._gpm.sample(ctx, rng)
        ctx.xpm        = self._xpm.sample(ctx, rng)
        ctx.match_time = self._match_time.sample(ctx, rng)

        match_id = self._next_match_id
        self._next_match_id += 1

        return TableFacts(
            match_id=match_id,
            player_id=player.player_id,
            hero_id=hero.hero_id,
            match_time=ctx.match_time,
            result=ctx.result,
            mmr_before=ctx.mmr_before,
            mmr_delta=ctx.mmr_delta,
            gpm=ctx.gpm,
            xpm=ctx.xpm,
            kills=ctx.kills,
            deaths=ctx.deaths,
            assists=ctx.assists,
            rampage=False,
            abandoned=anomaly == AnomalyKind.ABANDONED,
            report_received=False,
            commend_received=False,
            entered_low_priority=False,
        )



        