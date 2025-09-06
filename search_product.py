

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Setup
service = Service(r"F:\drivers\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service)

#open site
driver.get("https://dorjibari.com.bd/")
driver.maximize_window()

# Wait until menu is visible (use a stable locator, not li[10])
wait = WebDriverWait(driver, 10)

search_product = WebDriverWait(driver, 5).until(
    EC.element_to_be_clickable((By.ID,'Search-In-Modal-Classic'))
)
search_product.send_keys("panjabi" +Keys.RETURN )



time.sleep(8)
driver.quit()

