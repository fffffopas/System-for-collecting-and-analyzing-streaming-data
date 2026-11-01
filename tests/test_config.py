import pytest
from pydantic import ValidationError

from generator.config import GeneratorSettings


def test_defaults(monkeypatch):
    monkeypatch.delenv("GENERATOR_BATCH_SIZE", raising=False)
    assert GeneratorSettings(_env_file=None).batch_size == 1000


def test_env_override(monkeypatch):
    monkeypatch.setenv("GENERATOR_BATCH_SIZE", "7")
    assert GeneratorSettings(_env_file=None).batch_size == 7


def test_validation_rejects_bad_value(monkeypatch):
    monkeypatch.setenv("GENERATOR_ANOMALY_PROBABILITY", "5")
    with pytest.raises(ValidationError):
        GeneratorSettings(_env_file=None)