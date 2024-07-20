from functools import lru_cache

import twilio.rest

from app.settings import get_settings


@lru_cache
def get_twilio_client() -> twilio.rest.Client:
    settings = get_settings()
    return twilio.rest.Client(
        username=settings.twilio_account_sid,
        password=settings.twilio_account_auth_token.get_secret_value(),
    )


def send_text_message(*, to: str, body: str) -> None:
    get_twilio_client().messages.create(
        to=to,
        from_=get_settings().twilio_from_phone_number,
        body=body,
    )
