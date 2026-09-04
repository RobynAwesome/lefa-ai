from pydantic import AliasChoices, Field, SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    alpaca_api_key: SecretStr = Field(
        default=SecretStr(""),
        validation_alias=AliasChoices("ALPACA_API_KEY", "alpaca_api_key"),
    )
    alpaca_secret_key: SecretStr = Field(
        default=SecretStr(""),
        validation_alias=AliasChoices(
            "ALPACA_SECRET_KEY", "ALPACA_API_SECRET", "alpaca_secret_key", "alpaca_api_secret"
        ),
    )
    alpaca_paper: bool = Field(
        default=True,
        validation_alias=AliasChoices("ALPACA_PAPER_TRADE", "ALPACA_PAPER", "alpaca_paper"),
    )
    lefa_execution_enabled: bool = True

    @model_validator(mode="after")
    def enforce_paper_truth_lock(self) -> "Settings":
        if not self.alpaca_paper:
            raise ValueError("LEFA baseline prohibits live Alpaca connections; paper trading only")
        return self

