import time
import unittest
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

class DisasterBridgeUserFlowTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        self.base_url = "http://127.0.0.1:8000/"
        self.wait = WebDriverWait(self.driver, 15)

    def safe_click(self, element):
        """Scroll into view and click element safely with JS fallback."""
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        try:
            element.click()
        except Exception:
            self.driver.execute_script("arguments[0].click();", element)

    def test_signup_login_profile(self):
        driver = self.driver
        driver.get(self.base_url)

        print("Visiting homepage...")
        request_help_btn = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "REQUEST HELP"))
        )
        self.safe_click(request_help_btn)

        print("Filling signup form...")
        self.wait.until(EC.presence_of_element_located((By.NAME, "name")))

        # Unique user info
        name = f"Test User {random.randint(1000,9999)}"
        email = f"user{random.randint(1000,9999)}@example.com"
        phone = f"017{random.randint(10000000,99999999)}"
        password = "TestPassword123!"

        # Fill signup fields
        driver.find_element(By.NAME, "name").send_keys(name)
        driver.find_element(By.NAME, "email").send_keys(email)
        driver.find_element(By.NAME, "phone_number").send_keys(phone)
        Select(driver.find_element(By.NAME, "role")).select_by_visible_text("Victim")
        driver.find_element(By.NAME, "password1").send_keys(password)
        driver.find_element(By.NAME, "password2").send_keys(password)

        # Submit signup safely
        submit_btn = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        self.safe_click(submit_btn)

        print("Signup submitted. Navigating to login page...")

        # Explicitly go to login page to ensure login happens
        driver.get(self.base_url + "login/")  # replace "login/" with your actual login URL

        # Wait for login form fields
        login_email_input = self.wait.until(
            EC.presence_of_element_located((By.NAME, "username"))
        )
        login_password_input = self.wait.until(
            EC.presence_of_element_located((By.NAME, "password"))
        )

        # Fill login form
        login_email_input.send_keys(email)
        login_password_input.send_keys(password)

        login_btn = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        self.safe_click(login_btn)

        print("Logged in successfully. Checking profile page...")

        # Check profile page heading
        profile_heading = self.wait.until(
            EC.presence_of_element_located((By.TAG_NAME, "h2"))
        )
        self.assertIn("Profile", profile_heading.text)

        print(f"✅ Signup + Login successful for: {email}")

    def tearDown(self):
        time.sleep(6)
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
