from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
from selenium.webdriver.common.action_chains import ActionChains

# Setup
service = Service(r"F:\\drivers\\chromedriver-win64\\chromedriver.exe")
driver = webdriver.Chrome(service=service)

driver.get("https://www.rokomari.com/")
driver.maximize_window()

wait = WebDriverWait(driver, 10)

# --- ✅ Added Safe Popup Handling ---
try:
    popup_banner = wait.until(EC.presence_of_element_located(
        (By.XPATH, "//button[@aria-label='Close']")
    ))
    driver.execute_script("arguments[0].click();", popup_banner)

    print("✅ Popup banner clicked")
except TimeoutException:
    print("❌ No popup banner found")

# ------select category -------
category = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//a[h2[normalize-space(text())='Dates (Khejur)']]")
    )
)

driver.execute_script(
        "window.scrollTo(0, arguments[0].getBoundingClientRect().top + window.scrollY - 120);",
        category
    )
time.sleep(0.5)
category.click()

# ------select product -------
product_item = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, "//img[@alt='Saad Maryam Premium Al Madinah Dates 500gm image']")
    )
)

driver.execute_script(
        "window.scrollTo(0, arguments[0].getBoundingClientRect().top + window.scrollY - 120);",
        product_item
)
time.sleep(0.5)
product_item.click()

# ------add to cart product -------

# Switch to the new tab
driver.switch_to.window(driver.window_handles[-1])  # last opened tab

# Now wait for Add to Cart
add_to_cart = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@product-id='450504' and contains(@class, 'add-to-cart-btn-details-page')]")))
add_to_cart.click()

# ------show the product -------
cart_page = wait.until(EC.element_to_be_clickable((By.ID, "js-cart-menu")))
cart_page.click()

time.sleep(10)
driver.quit()
