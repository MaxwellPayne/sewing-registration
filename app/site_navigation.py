import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import Select

from app import settings
from app.datastructures import CourseCapacityReport


def navigate_to_course_capacity(fresh_driver: webdriver.Chrome) -> CourseCapacityReport:
    _navigate_to_initial_landing_page(fresh_driver)
    _navigate_to_login_page(fresh_driver)
    _do_login(fresh_driver)
    _ensure_continuing_education_menu_page(fresh_driver)
    _click_register_and_pay_link(fresh_driver)
    _search_for_course(fresh_driver)
    return _obtain_course_capacity_info(fresh_driver)


def _navigate_to_initial_landing_page(driver: webdriver.Chrome) -> None:
    driver.get(settings.CONTINUING_EDUCATION_LANDING_PAGE)
    time.sleep(5)


def _navigate_to_login_page(driver: webdriver.Chrome) -> None:
    login_li_elem = driver.find_element(By.ID, "acctLogin")
    login_link_elem = login_li_elem.find_element(By.XPATH, "a")
    login_link: str = login_link_elem.get_attribute("href")

    driver.get(login_link)
    time.sleep(5)


def _do_login(driver: webdriver.Chrome) -> None:
    login_form = driver.find_element(By.NAME, "datatelform")
    username_input = login_form.find_element(By.ID, "USER_NAME")
    password_input = login_form.find_element(By.ID, "CURR_PWD")
    submit_input = login_form.find_element(By.NAME, "SUBMIT2")

    username_input.send_keys(settings.USERNAME)
    password_input.send_keys(settings.PASSWORD)
    submit_input.click()
    time.sleep(5)


def _ensure_continuing_education_menu_page(driver: webdriver.Chrome) -> None:
    """
    Sometimes the login submit button takes us to "Main Menu" rather than a page specific to Continuing Education. If
    that happened, this function ensures that we navigate to Continuing Education.
    """
    if len(driver.find_elements(By.ID, "bodyConstituency")) > 0:
        # already on the proper page
        return

    persona_a_tag: WebElement | None = None
    for persona_box_li in driver.find_elements(By.CLASS_NAME, "WBCE_Boxes"):
        persona_a_tag = persona_box_li.find_element(By.TAG_NAME, "a")
        if persona_a_tag.text == "Continuing Education":
            break

    if persona_a_tag is None:
        raise Exception("'Continuing Education' picture box not found")

    persona_a_tag.click()
    time.sleep(5)


def _click_register_and_pay_link(driver: webdriver.Chrome) -> None:
    registration_div = driver.find_element(By.CLASS_NAME, "left")
    for span in registration_div.find_elements(By.TAG_NAME, "span"):
        if span.text == "Register and Pay for Continuing Education Classes":
            break
    else:
        raise Exception("Register and pay link not found")

    register_and_pay_link = span.find_element(By.XPATH, "..")
    register_and_pay_link.click()
    time.sleep(5)


def _search_for_course(driver: webdriver.Chrome) -> None:
    identify_your_classes_table = driver.find_element(By.ID, "GROUP_Grp_LIST_VAR1").find_element(By.TAG_NAME, "table")

    course_prefix_select = Select(identify_your_classes_table.find_element(By.ID, "LIST_VAR1_1"))
    course_prefix_select.select_by_value(settings.COURSE_PREFIX)

    course_number_input = identify_your_classes_table.find_element(By.ID, "LIST_VAR2_1")
    course_number_input.send_keys(settings.COURSE_NUMBER)

    submit_input = driver.find_element(By.NAME, "SUBMIT2")
    submit_input.click()

    time.sleep(15)


def _obtain_course_capacity_info(driver: webdriver.Chrome) -> CourseCapacityReport:
    courses_tbody = driver.find_element(By.ID, "GROUP_Grp_LIST_VAR1").find_element(By.TAG_NAME, "tbody")

    tr: WebElement
    for idx, tr in enumerate(courses_tbody.find_elements(By.TAG_NAME, "tr")):
        if idx == 0:
            continue

        found_desired_campus = False
        for td in tr.find_elements(By.TAG_NAME, "td"):
            for p in td.find_elements(By.TAG_NAME, "p"):
                if p.text == settings.COURSE_CAMPUS_LOCATION:
                    found_desired_campus = True

        if found_desired_campus:
            break
    else:
        raise Exception(f"Could not find a course for campus '{settings.COURSE_CAMPUS_LOCATION}'")

    # looks like "12 / 0"
    course_capacity_text = tr.find_elements(By.TAG_NAME, "td")[-1].text
    capacity, available_seats = course_capacity_text.replace(" ", "").split("/")
    return CourseCapacityReport(
        capacity=int(capacity),
        available_seats=int(available_seats),
    )
