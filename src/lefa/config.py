from pydantic import SecretStr, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    alpaca_api_key: SecretStr
    alpaca_secret_key: SecretStr
    alpaca_paper: bool = True
    lefa_execution_enabled: bool = False

    @model_validator(mode="after")
    def enforce_paper_truth_lock(self) -> "Settings":
        if not self.alpaca_paper:
            raise ValueError("LEFA baseline prohibits live Alpaca connections")
        if self.lefa_execution_enabled:
            raise ValueError("LEFA baseline has no execution authority")
        return self
