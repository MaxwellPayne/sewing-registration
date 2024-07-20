import requests

from app.settings import get_settings


def send_email(*, to: str, subject: str, text: str) -> None:
    settings = get_settings()
    endpoint = f"https://api.mailgun.net/v3/{settings.mailgun_sending_domain}/messages"
    res = requests.post(
        endpoint,
        auth=("api", settings.mailgun_api_key.get_secret_value()),
        data={
            "from": f"Mailgun Course Finder <postmaster@{settings.mailgun_sending_domain}>",
            "to": to,
            "subject": subject,
            "text": text,
        },
    )
    res.raise_for_status()
