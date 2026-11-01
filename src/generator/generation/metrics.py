from __future__ import annotations

import random
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timedelta

from generator.generation import defaults
from generator.generation.anomaly import AnomalyKind  # указал корректный импорт
from generator.models import Hero, Player


@dataclass(frozen=True, slots=True)
class DotaProfile:
    """Статическая конфигурация предметной области Dota 2.
    
    Одинакова для всех матчей. Не знает о конкретном игроке или герое —
    только о том, «как устроен мир».
    """
    region_mmr_mean: dict[str, int] = field(default_factory=lambda: dict(defaults.REGION_MMR_MEAN))
    hero_role_weights: dict[str, tuple[float, ...]] = field(default_factory=lambda: dict(defaults.HERO_ROLE_WEIGHTS))
    hero_gpm_mean: dict[str, float] = field(default_factory=lambda: dict(defaults.HERO_GPM_MEAN))
    hero_xpm_mean: dict[str, float] = field(default_factory=lambda: dict(defaults.HERO_XPM_MEAN))
    role_kills_base: dict[str, float] = field(default_factory=lambda: dict(defaults.ROLE_KILLS_BASE))
    role_deaths_base: dict[str, float] = field(default_factory=lambda: dict(defaults.ROLE_DEATHS_BASE))
    role_assists_base: dict[str, float] = field(default_factory=lambda: dict(defaults.ROLE_ASSISTS_BASE))
    side_win_bonus: dict[str, float] = field(default_factory=lambda: dict(defaults.SIDE_WIN_BONUS))
    hero_winrate_bonus: dict[str, float] = field(default_factory=lambda: dict(defaults.HERO_WINRATE_BONUS))
    
    # === Длительность матча ===
    match_time_mean_min: float = 40.0
    match_time_std_min: float = 10.0
    match_time_min_min: float = 20.0
    match_time_max_min: float = 90.0
    
    # === MMR delta ===
    mmr_delta_win: int = 25
    mmr_delta_lose: int = -25
    mmr_delta_std: float = 5.0
    kda_bonus_max: float = 10.0
    
    # === Вероятности редких событий ===
    rampage_probability: float = 0.003
    base_report_probability: float = 0.10
    base_commend_probability: float = 0.12
    low_priority_base_probability: float = 0.005
    
    # === Прочее ===
    mmr_noise_std: float = 200.0   
    gpm_noise_std: float = 80.0
    xpm_noise_std: float = 70.0

@dataclass(slots=True)
class MatchContext:
    at: datetime
    player: Player
    hero: Hero

    role: str = ""
    side: str = ""
    mmr_delta: int = 0
    result: bool = False
    kills: int = 0
    deaths: int = 0
    assists: int = 0

    gpm: float = 0.0
    xpm: float = 0.0
    match_time: timedelta = timedelta(0)
    anomaly: AnomalyKind | None = None


def _clamp(value: float, low: float, high: float) -> float:
    return max(low, min(high, value))


class MetricSampler(ABC):

    @abstractmethod
    def sample(self, ctx: MatchContext, rng: random.Random): ...

# убрал MmrBeforeSample

class SideSampler(MetricSampler):
    def __init__(self, profile: DotaProfile) -> None:
        self._profile = profile

    def sample(self, ctx: MatchContext, rng: random.Random) -> str:
        return rng.choice(defaults.SIDES)

class RoleSampler(MetricSampler):
    def __init__(self, profile: DotaProfile) -> None:
        self._profile = profile

    def sample(self, ctx: MatchContext, rng: random.Random) -> str:
        weights = self._profile.hero_role_weights.get(
            ctx.hero.hero_name, defaults.DEFAULT_ROLE_WEIGHTS
        )
        return rng.choices(defaults.ROLES, weights=weights, k=1)[0]

class ResultsSample(MetricSampler):
    def __init__(self, profile: DotaProfile) -> None:
        self._profile = profile
    
    def sample(self, ctx: MatchContext, rng: random.Random) -> bool:
        base_winrate = 0.5
        base_winrate += self._profile.side_win_bonus.get(ctx.side, 0.0)
        base_winrate += self._profile.hero_winrate_bonus.get(ctx.hero.hero_name, defaults.DEFAULT_HERO_WINRATE_BONUS)
        base_winrate = _clamp(base_winrate, 0.05, 0.95)
        return rng.random() < base_winrate

class KillsSample(MetricSampler): 
    def __init__(self, profile: DotaProfile) -> None:
        self._profile = profile
    
    def sample(self, ctx: MatchContext, rng: random.Random) -> int:
        role = ctx.role
        base = self._profile.role_kills_base[role]
        multiplier = 1.3 if ctx.result else 0.8
        noise = rng.gauss(0, 2.0)
        value = base * multiplier + noise
        return max(0, round(value))


class DeathsSample(MetricSampler):
    def __init__(self, profile: DotaProfile) -> None:
        self._profile = profile

    def sample(self, ctx: MatchContext, rng: random.Random) -> int:
        role = ctx.role
        base = self._profile.role_deaths_base[role]
        multiplier = 0.8 if ctx.result else 1.3
        noise = rng.gauss(0, 1.5)
        return max(0, round(base * multiplier + noise))

class AssistsSample(MetricSampler):
    def __init__(self, profile: DotaProfile) -> None:
        self._profile = profile

    def sample(self, ctx: MatchContext, rng: random.Random) -> int:
        role = ctx.role
        base = self._profile.role_assists_base[role]
        multiplier = 1.2 if ctx.result else 0.9
        noise = rng.gauss(0, 2.0)
        return max(0, round(base * multiplier + noise))

class MmrDeltaSample(MetricSampler):
    
    def __init__(self, profile: DotaProfile) -> None:
        self._profile = profile
    
    def sample(self, ctx: MatchContext, rng: random.Random) -> int:
        base = self._profile.mmr_delta_win if ctx.result else self._profile.mmr_delta_lose
        
        kda = (ctx.kills + ctx.assists) / max(1, ctx.deaths)

        kda_factor = _clamp((kda - 3.0) / 3.0, -1.0, 1.0)  # [-1, 1]
        kda_bonus = kda_factor * self._profile.kda_bonus_max
        
        if not ctx.result:
            kda_bonus = -kda_bonus
        noise = rng.gauss(0, self._profile.mmr_delta_std)
        
        return round(base + kda_bonus + noise)

class GpmSampler(MetricSampler):
    
    def __init__(self, profile: DotaProfile) -> None:
        self._profile = profile
    
    def sample(self, ctx: MatchContext, rng: random.Random) -> float:
        base = self._profile.hero_gpm_mean.get(ctx.hero.hero_name, defaults.DEFAULT_GPM)
        win_bonus = 50.0 if ctx.result else 0.0
        noise = rng.gauss(0, self._profile.gpm_noise_std)
        return round(_clamp(base + win_bonus + noise, 50.0, 1500.0), 1)


class XpmSampler(MetricSampler):
    
    def __init__(self, profile: DotaProfile) -> None:
        self._profile = profile
    
    def sample(self, ctx: MatchContext, rng: random.Random) -> float:
        base = self._profile.hero_xpm_mean.get(ctx.hero.hero_name, defaults.DEFAULT_XPM)
        win_bonus = 50.0 if ctx.result else 0.0
        noise = rng.gauss(0, self._profile.xpm_noise_std)
        return round(_clamp(base + win_bonus + noise, 50.0, 1500.0), 1)

class MatchTimeSampler(MetricSampler):
    
    def __init__(self, profile: DotaProfile) -> None:
        self._profile = profile
    
    def sample(self, ctx: MatchContext, rng: random.Random) -> timedelta:
        base = self._profile.match_time_mean_min
        win_bonus = 3.0 if ctx.result else -3.0
        
        noise = rng.gauss(0, self._profile.match_time_std_min)

        minutes = _clamp(
            base + win_bonus + noise,
            self._profile.match_time_min_min,   # 20
            self._profile.match_time_max_min,   # 90
        )
        
        return timedelta(minutes=minutes)