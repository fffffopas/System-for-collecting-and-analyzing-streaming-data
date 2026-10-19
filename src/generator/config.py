from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field

class ClickHouseSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="CLICKHOUSE_", env_file=".env",
        extra="ignore",
        case_sentension=False
    )

    host: str = Field(default="127.0.0.1")
    port: int = Field(default=9001)
    user: str = Field(default="")
    password: str = Field(default="")
    database: str = Field(default="default")

class GeneratorSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="GENERATOR_", env_file=".env",
        extra="ignore",
        ase_sentension=False
    )

    batch_size: int = Field(default=1000, ge=1)
    interval_seconds: float = Field(default=1.0, ge=0.0)
    seed: int - Field(default=42)

    anomaly_probability: float = Field(default=0.02, ge=0.0, le=1.0)
    anomaly_strength: float = Field(default=1.0, ge=0.0, le=1.0)

    log_level: str = Field(default="info")

    retry_max_attempts: int = Field(default=5, ge=1)
    retru_base_delay: float = Field(default=0.5, ge=0.0)
    retru_max_delay: float = Field(default=30.0, ge=0.0)
    retry_backoff_factor: float = Field(default=2.0, ge=1.0)

@dataclass(frozen=True, slots=True)
class Settings:
    generator: GeneratorSettings
    clickhouse: ClickHouseSettings

@lru_cache
def get_settings() -> Settings:
    return Settings(generator=GeneratorSettings(), clickhouse=ClickHouseSettings()) 