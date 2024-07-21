import argparse
import logging
import sys
from contextlib import suppress

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import app.notifications
from app.datastructures import CourseCapacityReport
from app.settings import get_settings
from app.site_navigation import navigate_to_course_capacity


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt="%Y-%m-%d %H:%M:%S%z",
    handlers=[logging.StreamHandler(sys.stdout)],
)


def _main() -> None:
    _ = get_settings()

    parser = argparse.ArgumentParser()
    parser.add_argument("--show-gui", default=False, action="store_true")
    args = parser.parse_args()

    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    if not args.show_gui:
        options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)

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
    _main()


"""
TODO:
- Better sleep with WebDriverWait
"""
