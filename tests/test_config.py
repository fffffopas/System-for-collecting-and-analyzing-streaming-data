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


def test_players_count_default():
    assert GeneratorSettings(_env_file=None).players_count == 500


def test_log_level_is_normalized(monkeypatch):
    monkeypatch.setenv("GENERATOR_LOG_LEVEL", "debug")
    assert GeneratorSettings(_env_file=None).log_level == "DEBUG"


def test_log_level_rejects_garbage(monkeypatch):
    monkeypatch.setenv("GENERATOR_LOG_LEVEL", "LOUD")
    with pytest.raises(ValidationError):
        GeneratorSettings(_env_file=None)


def test_retry_env_names(monkeypatch):
    monkeypatch.setenv("GENERATOR_RETRY_BASE_DELAY", "2.5")
    assert GeneratorSettings(_env_file=None).retry_base_delay == 2.5
