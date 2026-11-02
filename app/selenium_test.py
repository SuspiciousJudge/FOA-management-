"""
Selenium tests for food ordering app login page.
Uses https://www.saucedemo.com as a demo login site.
Swap BASE_URL and credentials for your actual site.
"""

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

DELAY = 2  # seconds between steps so you can see what is happening


@pytest.fixture
def driver():
    options = webdriver.ChromeOptions()
    # remove headless so you can watch the browser
    dr = webdriver.Chrome(options=options)
    dr.maximize_window()
    yield dr
    time.sleep(DELAY)
    dr.quit()


class TestLogin:

    def test_valid_login(self, driver):
        """Valid credentials should land on the products page."""
        print("\n[TEST] Valid login")

        driver.get(BASE_URL)
        time.sleep(DELAY)

        # fill username
        wait = WebDriverWait(driver, 10)
        user_field = wait.until(EC.presence_of_element_located((By.ID, "user-name")))
        user_field.clear()
        user_field.send_keys(VALID_USER)
        time.sleep(1)

        # fill password
        pass_field = driver.find_element(By.ID, "password")
        pass_field.clear()
        pass_field.send_keys(VALID_PASS)
        time.sleep(1)

        # click login
        driver.find_element(By.ID, "login-button").click()
        time.sleep(DELAY)

        # verify we are on the products page
        wait.until(EC.url_contains("inventory"))
        heading = wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "title"))
        )
        assert "Products" in heading.text, f"Expected 'Products' heading, got: {heading.text}"
        print(f"[PASS] Logged in — page title: {heading.text}")
        time.sleep(DELAY)


    def test_invalid_username(self, driver):
        """Wrong username should show an error message."""
        print("\n[TEST] Invalid username")

        driver.get(BASE_URL)
        time.sleep(DELAY)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "user-name"))).send_keys(INVALID_USER)
        time.sleep(1)
        driver.find_element(By.ID, "password").send_keys(VALID_PASS)
        time.sleep(1)
        driver.find_element(By.ID, "login-button").click()
        time.sleep(DELAY)

        # error container must appear
        error = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        )
        assert "Username and password do not match" in error.text or \
               "do not match" in error.text, \
               f"Unexpected error text: {error.text}"
        print(f"[PASS] Error shown: {error.text}")
        time.sleep(DELAY)


    def test_invalid_password(self, driver):
        """Wrong password should show an error message."""
        print("\n[TEST] Invalid password")

        driver.get(BASE_URL)
        time.sleep(DELAY)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "user-name"))).send_keys(VALID_USER)
        time.sleep(1)
        driver.find_element(By.ID, "password").send_keys(INVALID_PASS)
        time.sleep(1)
        driver.find_element(By.ID, "login-button").click()
        time.sleep(DELAY)

        error = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        )
        assert "do not match" in error.text, f"Unexpected error text: {error.text}"
        print(f"[PASS] Error shown: {error.text}")
        time.sleep(DELAY)


    def test_empty_credentials_rejected(self, driver):
        """Submitting empty form should show a required-field error."""
        print("\n[TEST] Empty credentials")

        driver.get(BASE_URL)
        time.sleep(DELAY)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "login-button"))).click()
        time.sleep(DELAY)

        error = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        )
        assert "Username is required" in error.text, f"Unexpected error: {error.text}"
        print(f"[PASS] Rejected empty form: {error.text}")
        time.sleep(DELAY)


    def test_invalid_both_rejected(self, driver):
        """Both fields wrong — must stay on login page, no redirect."""
        print("\n[TEST] Both credentials invalid")

        driver.get(BASE_URL)
        time.sleep(DELAY)

        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "user-name"))).send_keys(INVALID_USER)
        time.sleep(1)
        driver.find_element(By.ID, "password").send_keys(INVALID_PASS)
        time.sleep(1)
        driver.find_element(By.ID, "login-button").click()
        time.sleep(DELAY)

        # must stay on login page — inventory should NOT be in URL
        assert "inventory" not in driver.current_url, "Should not have reached inventory page"

        error = wait.until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "[data-test='error']"))
        )
        assert len(error.text) > 0, "Error message should not be empty"
        print(f"[PASS] Rejected bad credentials: {error.text}")
        time.sleep(DELAY)
