import argparse
import logging
import sys
from contextlib import suppress

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

import app.notifications
from app.datastructures import CourseCapacityReport
from app.settings import get_settings
from app.site_navigation import navigate_to_course_capacity


if logging.getLogger().hasHandlers():
    logging.getLogger().setLevel(logging.INFO)
else:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt="%Y-%m-%d %H:%M:%S%z",
        handlers=[logging.StreamHandler(sys.stdout)],
    )


logger = logging.getLogger(__name__)


def handler(event, context) -> None:
    logger.info("Handler starts with event: %s", event)
    _ = get_settings()

    parser = argparse.ArgumentParser()
    parser.add_argument("--no-docker", default=False, action="store_true")
    args = parser.parse_args()

    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service: Service | None = None

    if not args.no_docker:
        # inspired by (https://medium.com/@kroeze.wb/running-selenium-in-aws-lambda-806c7e88ec64)
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-dev-tools")
        options.add_argument("--no-zygote")
        options.add_argument("--single-process")
        options.binary_location = "/opt/chrome/chrome-linux64/chrome"

        service = Service(
            executable_path="/opt/chrome-driver/chromedriver-linux64/chromedriver",
            service_log_path="/tmp/chromedriver.log",
        )

    logger.info("Initializing webdriver...")
    driver = webdriver.Chrome(
        options=options,
        service=service,
    )
    logger.info("Webdriver is initialized")

    capacity_report: CourseCapacityReport
    try:
        capacity_report = navigate_to_course_capacity(driver)
    except Exception:
        app.notifications.send_heartbeat_email()
        raise
    finally:
        driver.quit()

    if capacity_report.available_seats > 0:
        with suppress(Exception):
            app.notifications.send_bingo_emails(capacity_report)
        app.notifications.send_bingo_texts(capacity_report)
    else:
        app.notifications.send_heartbeat_email()


if __name__ == "__main__":
    handler(None, None)


"""
TODO:
- Better sleep with WebDriverWait
"""
