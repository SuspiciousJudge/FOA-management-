import time
import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://www.saucedemo.com"
VALID_USER = "standard_user"
VALID_PASS = "secret_sauce"
INVALID_USER = "wrong_user"
INVALID_PASS = "wrong_pass"

DELAY = 2


@pytest.fixture
def driver():
    dr = webdriver.Chrome()
    dr.maximize_window()
    yield dr
    time.sleep(DELAY)
    dr.quit()


class TestLogin:

    def test_valid_login(self, driver):
        driver.get(BASE_URL)
        time.sleep(DELAY)

        wait = WebDriverWait(driver, 10)
        user_field = wait.until(EC.presence_of_element_located((By.ID, "user-name")))
        user_field.clear()
        user_field.send_keys(VALID_USER)
        time.sleep(1)

        pass_field = driver.find_element(By.ID, "password")
        pass_field.clear()
        pass_field.send_keys(VALID_PASS)
        time.sleep(1)

        driver.find_element(By.ID, "login-button").click()
        time.sleep(DELAY)

        wait.until(EC.url_contains("inventory"))
        heading = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "title")))
        assert "Products" in heading.text
        time.sleep(DELAY)

    def test_invalid_username(self, driver):
        driver.get(BASE_URL)
        time.sleep(DELAY)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "user-name"))).send_keys(INVALID_USER)
        time.sleep(1)
        driver.find_element(By.ID, "password").send_keys(VALID_PASS)
        time.sleep(1)
        driver.find_element(By.ID, "login-button").click()
        time.sleep(DELAY)

        error = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']")))
        assert "do not match" in error.text
        time.sleep(DELAY)

    def test_invalid_password(self, driver):
        driver.get(BASE_URL)
        time.sleep(DELAY)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "user-name"))).send_keys(VALID_USER)
        time.sleep(1)
        driver.find_element(By.ID, "password").send_keys(INVALID_PASS)
        time.sleep(1)
        driver.find_element(By.ID, "login-button").click()
        time.sleep(DELAY)

        error = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']")))
        assert "do not match" in error.text
        time.sleep(DELAY)

    def test_empty_credentials_rejected(self, driver):
        driver.get(BASE_URL)
        time.sleep(DELAY)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "login-button"))).click()
        time.sleep(DELAY)

        error = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']")))
        assert "Username is required" in error.text
        time.sleep(DELAY)

    def test_invalid_both_rejected(self, driver):
        driver.get(BASE_URL)
        time.sleep(DELAY)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "user-name"))).send_keys(INVALID_USER)
        time.sleep(1)
        driver.find_element(By.ID, "password").send_keys(INVALID_PASS)
        time.sleep(1)
        driver.find_element(By.ID, "login-button").click()
        time.sleep(DELAY)

        assert "inventory" not in driver.current_url

        error = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']")))
        assert len(error.text) > 0
        time.sleep(DELAY)
