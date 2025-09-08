from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    database_url: str = Field(default="sqlite:///./pumpdex.db")
    pumpfun_api_base: str = Field(default="https://api.pumpfun.placeholder")
    pumpswap_api_base: str = Field(default="https://api.pumpswap.placeholder")
    index_interval_seconds: int = Field(default=20)

    class Config:
        env_file = ".env"

settings = Settings()
