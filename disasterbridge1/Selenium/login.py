from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# 1️⃣ Start Browser
driver = webdriver.Chrome()  # Use Edge() or Firefox() if needed
driver.maximize_window()

# 2️⃣ Open Login Page
driver.get("http://127.0.0.1:8000/login/")

# 3️⃣ Fill login fields
driver.find_element(By.NAME, "username").send_keys("priyam@gmail.com")
driver.find_element(By.NAME, "password").send_keys("1234")

# 4️⃣ Click on the login button
driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

# 5️⃣ Wait a few seconds for redirect or message
time.sleep(3)

# 6️⃣ Verify login success (redirect to dashboard or home)
if "dashboard" in driver.current_url.lower():
    print("✅ Login test passed! Redirected to dashboard.")
elif "logout" in driver.page_source.lower() or "welcome" in driver.page_source.lower():
    print("✅ Login success message found.")
elif "invalid" in driver.page_source.lower() or "error" in driver.page_source.lower():
    print("❌ Login failed - invalid credentials message shown.")
else:
    print("❌ Login test failed - no success indicator found.")

# 7️⃣ Close browser
driver.quit()
