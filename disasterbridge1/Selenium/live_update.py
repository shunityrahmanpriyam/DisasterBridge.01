from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# 1️⃣ Launch browser
driver = webdriver.Chrome()
driver.maximize_window()

# 2️⃣ Open homepage
driver.get("http://127.0.0.1:8000/")

# 3️⃣ Wait for page to load
time.sleep(2)

try:
    # 4️⃣ Find and click the UPDATES link from navbar
    updates_link = driver.find_element(By.LINK_TEXT, "UPDATES")
    updates_link.click()
    print("🔹 Clicked on 'UPDATES' link from navbar.")
except Exception as e:
    print("❌ Could not find 'UPDATES' link in navbar!", e)
    driver.quit()
    exit()

# 5️⃣ Wait for redirect
time.sleep(3)

# 6️⃣ Verify that Live Updates page loaded successfully
if "/updates" in driver.current_url.lower():
    print("✅ Successfully navigated to the Live Updates page.")
elif "live updates" in driver.page_source.lower():
    print("✅ Live Updates content found on the page.")
else:
    print("❌ Failed to load the Live Updates page.")

# 7️⃣ Optional: Check if message shown (no updates)
if "no live updates" in driver.page_source.lower():
    print("ℹ️ Message shown: No live updates available right now.")
else:
    print("✅ Live update cards or content detected.")

# 8️⃣ Close browser
time.sleep(2)
driver.quit()
