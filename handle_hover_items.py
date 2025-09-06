from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
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
        (By.XPATH, '//*[@id="ts-desktop-home-page"]/div/div/div[3]/div/button')
    ))
    driver.execute_script("arguments[0].click();", popup_banner)
    print("✅ Popup banner clicked")
except TimeoutException:
    print("❌ No popup banner found")

# ------------------------------

book_item = wait.until(EC.presence_of_element_located(
    (By.XPATH, '//*[@id="ts--desktop-menu"]/div[1]/a[2]')
))
actions = ActionChains(driver)
actions.move_to_element(book_item).click().perform()
# book_item.click()

menu_item_hover = wait.until(EC.presence_of_element_located(
    (By.XPATH, '//*[@id="ts--desktop-menu"]/div[2]/div/div[1]/a/span[1]')
))

# Hover over the menu
actions = ActionChains(driver)
actions.move_to_element(menu_item_hover).perform()
time.sleep(2)

# Now locate a submenu item
submenu_item = wait.until(EC.element_to_be_clickable((
    By.XPATH, "//a[text()='হুমায়ূন আহমেদ']"
)))
submenu_item.click()

print("✅ Hover and submenu click successful!")

# --- ✅ Handle popup after navigation ---
try:
    popup_banner = WebDriverWait(driver, 5).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="js--entry-popup"]/div[1]/button'))
    )
    driver.execute_script("arguments[0].click();", popup_banner)
    print("✅ Second popup banner closed")
except TimeoutException:
    print("❌ No popup banner found after navigation")

# --- ✅ Select categories safely ---
try:
    category = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="js--categoryIds"]/div[1]/label'))
    )

    # Scroll slightly below header (offset by 100px)
    driver.execute_script("window.scrollTo(0, arguments[0].getBoundingClientRect().top + window.scrollY - 100);",
                          category)
    time.sleep(1)
    category.click()
    print("✅ First category clicked")

except Exception as e:
    print(f"⚠️ Failed to click first category: {e}")

try:
    category_two = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="js--categoryIds"]/div[3]/label'))
    )
    # Scroll element slightly below sticky header (120px offset)
    driver.execute_script(
        "window.scrollTo(0, arguments[0].getBoundingClientRect().top + window.scrollY - 120);",
        category_two
    )
    time.sleep(0.5)
    category_two.click()
    print("✅ Second category clicked")
except Exception as e:
    # Fallback to ActionChains click
    from selenium.webdriver.common.action_chains import ActionChains
    actions = ActionChains(driver)
    actions.move_to_element(category_two).click().perform()
    print(f"⚡ Second category clicked via ActionChains due to: {e}")



# click to go next page
next_page = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '/html/body/div[8]/div/div/div/section[3]/div[3]/a[2]'))
    )

# Scroll slightly below header (offset by 100px)
driver.execute_script("window.scrollTo(0, arguments[0].getBoundingClientRect().top + window.scrollY - 100);",
                          next_page)
time.sleep(1)
next_page.click()

time.sleep(10)
driver.quit()
