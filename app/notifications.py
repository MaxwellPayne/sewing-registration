import datetime
import logging
import traceback
import sys
import zoneinfo

from app import constants
from app.datastructures import CourseCapacityReport
from app.mailgun import send_email
from app.settings import get_settings
from app.twilio import send_text_message


logger = logging.getLogger(__name__)


def send_bingo_emails(capacity_report: CourseCapacityReport) -> None:
    """
    Send emails notifying that there is, in fact, availability for the course
    """
    settings = get_settings()
    for recipient in settings.bingo_notification_email_recipients:
        try:
            send_email(
                to=recipient,
                subject=constants.BINGO_EMAIL_SUBJECT,
                text=(
                    f"The class now has {capacity_report.available_seats} seat(s) available out of "
                    f"{capacity_report.capacity} total spots!"
                ),
            )
        except Exception:
            logger.exception("Unexpected error while sending BINGO email", extra={
                "capacity_report": capacity_report,
            })


def send_heartbeat_email() -> None:
    """
    Send an email updating the webmaster about the status of the program. This function implies that no availability
    for the course was found.
    """
    settings = get_settings()
    now_dt = datetime.datetime.now(datetime.UTC).astimezone(zoneinfo.ZoneInfo("America/Chicago"))
    now_dt_str = now_dt.strftime("%B %d, %H:%M:%S %Z")

    text: str
    if sys.exc_info() == (None, None, None):
        text = "Successfully scanned for course, and found no availability."
    else:
        text = "UNEXPECTED ERROR:\n" + traceback.format_exc()

    send_email(
        to=settings.webmaster_email,
        subject=f"Course Heartbeat at {now_dt_str}",
        text=text,
    )


def send_bingo_texts(capacity_report: CourseCapacityReport) -> None:
    # TODO: actual stuff
    return
    body: str = (
        f"The class now has {capacity_report.available_seats} seat(s) available out of "
        f"{capacity_report.capacity} total spots!"
    )

    for to_email in get_settings().bingo_notification_text_recipients:
        try:
            send_text_message(
                to=to_email,
                body=body,
            )
        except Exception:
            logger.exception(
                "Unexpected error whiles sending BINGO text message",
                extra={
                    "capacity_report": capacity_report,
                },
            )
