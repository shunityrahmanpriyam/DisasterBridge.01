
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

from selenium.webdriver.common.by import By
from selenium.webdriver import Keys

# Initialize Chrome WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Open Google
driver.get("http://127.0.0.1:8000/signup/")

# Find the search box by its element ID
googleSearchBox = driver.find_element(By.ID, value="id_name")

# Type a search query
googleSearchBox.send_keys("Ria")

# Wait for a few seconds
time.sleep(5)

# Close and quit the browser
driver.close()
driver.quit()