from __future__ import annotations

import enum
import random


class AnomalyKind(enum.StrEnum):
    ABANDONED = "abandoned"
    CHEATER_ALLIES = "cheater_allies"
    CHEATER_RIVAL = "cheater_rival"
    BLACKOUT = "blackout"

_ANOMALY_WEIGHTS = {
    AnomalyKind.ABANDONED: 0.50,
    AnomalyKind.CHEATER_ALLIES: 0.30,
    AnomalyKind.CHEATER_RIVAL: 0.15,
    AnomalyKind.BLACKOUT: 0.05,
}

class AnomalyPolicy:

    def __init__(self, probability: float, strength: float)->None:
        self._probability = probability
        self._strength = strength

    @property
    def strength(self) -> float:
        return self._strength

    def decide(self, rng: random.Random) -> AnomalyKind | None:
        if rng.random() >= self._probability:
            return None
        return rng.choices(
          list(_ANOMALY_WEIGHTS),
           weights=list(_ANOMALY_WEIGHTS.values()),
           k=1,
        )[0]