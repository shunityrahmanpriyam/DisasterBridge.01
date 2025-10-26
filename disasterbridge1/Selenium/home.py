
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import time

# Initialize Chrome WebDriver
driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

# Open a webpage
driver.get("http://127.0.0.1:8000/")

# Wait for 5 seconds
time.sleep(5)

# Close and quit the browser
driver.close()
driver.quit()