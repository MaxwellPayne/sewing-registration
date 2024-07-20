from __future__ import annotations
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


@lru_cache
def get_settings() -> Settings:
    return Settings()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    acc_username: str
    acc_password: str

    mailgun_api_key: str
    mailgun_sending_domain: str = "sandbox52cae161a59f4077bc37fc6a992a26aa.mailgun.org"

    webmaster_email: str
    bingo_notification_email_recipients: list[str]
