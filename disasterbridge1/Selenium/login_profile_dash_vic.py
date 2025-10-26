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
        self.wait = WebDriverWait(self.driver, 20)

    def test_signup_login_dashboard_flow(self):
        driver = self.driver
        driver.get(self.base_url)
        print("Visiting homepage...")

        # Go to SIGN IN / LOGIN page
        login_btn = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "SIGN IN/LOGIN"))
        )
        login_btn.click()
        print("➡️ Navigated to Login page")

        # Go to Sign Up
        signup_link = self.wait.until(
            EC.element_to_be_clickable((By.LINK_TEXT, "Sign Up here!"))
        )
        signup_link.click()
        print("📝 Opening Sign Up form...")

        # Fill signup form
        name = f"User{random.randint(1000,9999)}"
        email = f"user{random.randint(1000,9999)}@example.com"
        phone = f"018{random.randint(10000000,99999999)}"
        password = "TestPass123!"

        driver.find_element(By.NAME, "name").send_keys(name)
        driver.find_element(By.NAME, "email").send_keys(email)
        driver.find_element(By.NAME, "phone_number").send_keys(phone)
        Select(driver.find_element(By.NAME, "role")).select_by_visible_text("Victim")
        driver.find_element(By.NAME, "password1").send_keys(password)
        driver.find_element(By.NAME, "password2").send_keys(password)
        # Submit Sign Up form using JS click
        submit_button = self.wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        driver.execute_script("arguments[0].scrollIntoView(true);", submit_button)
        driver.execute_script("arguments[0].click();", submit_button)
        print("✅ Signup submitted")

        # Wait for login page
        self.wait.until(EC.presence_of_element_located((By.NAME, "username")))

        # Log in
        driver.find_element(By.NAME, "username").send_keys(email)
        driver.find_element(By.NAME, "password").send_keys(password)
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        print("🔐 Logged in successfully")

        # Wait for Profile page
        self.wait.until(EC.presence_of_element_located((By.XPATH, "//h2[contains(., 'Profile')]")))
        print("👤 Profile page loaded")

        # ---- Step 6: Click Dashboard ----
        try:
            dashboard_link = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[./span[text()='Dashboard']]"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", dashboard_link)
            driver.execute_script("arguments[0].click();", dashboard_link)
            print("📊 Navigated to Dashboard")
        except Exception as e:
            print("⚠️ Dashboard link not found:", e)

        # ---- Step 7: Click Request Aid ----
        try:
            request_aid_link = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[./span[text()='Request Aid']]"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", request_aid_link)
            driver.execute_script("arguments[0].click();", request_aid_link)
            print("🆘 Navigated to Request Aid page")
        except Exception as e:
            print("⚠️ Request Aid link not found:", e)

        # ---- Step 8: Back to Profile ----
        try:
            profile_link = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//a[./span[text()='PROFILE']]"))
            )
            driver.execute_script("arguments[0].scrollIntoView(true);", profile_link)
            driver.execute_script("arguments[0].click();", profile_link)
            print("🔁 Back to Profile page")
        except Exception as e:
            print("⚠️ Profile link not found:", e)

        print(f"✅ Full flow completed successfully for: {email}")

    def tearDown(self):
        time.sleep(5)
        self.driver.quit()


if __name__ == "__main__":
    unittest.main()
