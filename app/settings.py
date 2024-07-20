from __future__ import annotations
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


@lru_cache
def get_settings() -> Settings:
    return Settings()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    username: str
    password: str
