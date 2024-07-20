from __future__ import annotations
from functools import lru_cache

import pydantic
import pydantic_extra_types.phone_numbers
from pydantic_settings import BaseSettings, SettingsConfigDict


class PhoneNumberE164(pydantic_extra_types.phone_numbers.PhoneNumber):
    phone_format = "E164"


@lru_cache
def get_settings() -> Settings:
    return Settings()


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env')

    acc_username: str
    acc_password: str

    mailgun_api_key: pydantic.SecretStr
    mailgun_sending_domain: str = "sandbox52cae161a59f4077bc37fc6a992a26aa.mailgun.org"

    twilio_account_sid: str
    twilio_account_auth_token: pydantic.SecretStr
    twilio_from_phone_number: PhoneNumberE164 = "+18552592431"

    webmaster_email: str
    bingo_notification_email_recipients: list[str]

    bingo_notification_text_recipients: list[PhoneNumberE164] = pydantic.Field(min_items=1)
