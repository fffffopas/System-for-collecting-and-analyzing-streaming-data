import pytest

from generator.retry import RetryError, RetryPolicy


def test_success_first_try():
    policy = RetryPolicy(3, 0.5, 30, sleep=lambda s: None)
    assert policy.execute(lambda: 42) == 42


def test_retries_then_succeeds():
    calls = {"n": 0}

    def flaky():
        calls["n"] += 1
        if calls["n"] < 3:
            raise ConnectionError("fail")
        return "ok"

    slept = []
    policy = RetryPolicy(5, 0.5, 30, jitter=0.0, sleep=slept.append)
    assert policy.execute(flaky) == "ok"
    assert slept == [0.5, 1.0]         


def test_gives_up():
    policy = RetryPolicy(3, 0.1, 1, sleep=lambda s: None)
    with pytest.raises(RetryError):
        policy.execute(lambda: 1 / 0)