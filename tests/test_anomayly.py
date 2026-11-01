import random

from generator.generation.anomaly import AnomalyKind, AnomalyPolicy


def test_probability_zero_never_anomaly():
    p = AnomalyPolicy(0.0, 1.0)
    rng = random.Random(1)
    assert all(p.decide(rng) is None for _ in range(1000))


def test_probability_one_always_anomaly():
    p = AnomalyPolicy(1.0, 1.0)
    rng = random.Random(1)
    assert all(isinstance(p.decide(rng), AnomalyKind) for _ in range(100))