import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Inline credentials (⚠️ not secure, just for testing)
USER_EMAIL = "Mail"
USER_PASS = "pass"

driver = webdriver.Chrome()
driver.get("https://www.rokomari.com/")
driver.maximize_window()

wait = WebDriverWait(driver, 15)

# Close popup if it shows
try:
    wait.until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class,'modal_modalCloseButton')]")
        )
    ).click()
except:
    pass

# Click Sign In
sign_in = wait.until(
    EC.presence_of_element_located((By.XPATH, "//a[contains(@class,'SignIn')]"))
)
driver.execute_script("arguments[0].click();", sign_in)

# Click Google login
wait.until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'btn-social-google')]"))
).click()

# --- Switch to Google login popup ---
main_window = driver.current_window_handle
for handle in driver.window_handles:
    if handle != main_window:
        driver.switch_to.window(handle)
        break

# --- Enter email ---
email_box = wait.until(EC.presence_of_element_located((By.ID, "identifierId")))
email_box.send_keys(USER_EMAIL)

# Click Next after email
next_button_email = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']"))
)
next_button_email.click()

# --- Enter password ---
password_box = wait.until(EC.presence_of_element_located((By.NAME, "Passwd")))
password_box.send_keys(USER_PASS)

# Click Next after password
next_button_pass = wait.until(
    EC.element_to_be_clickable((By.XPATH, "//span[text()='Next']"))
)
next_button_pass.click()

time.sleep(5)  # wait for login to process