from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from app.datastructures import CourseCapacityReport
from app.settings import get_settings
from app.site_navigation import navigate_to_course_capacity


def _main() -> None:
    _ = get_settings()

    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    capacity_report: CourseCapacityReport | None = None
    try:
        capacity_report = navigate_to_course_capacity(driver)
    finally:
        driver.quit()

    if capacity_report is not None:
        print("CAPACITY...", capacity_report)


if __name__ == "__main__":
    _main()


"""
TODO:
- Better sleep with WebDriverWait
"""
