import imaplib, email, re, time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup  # pip install beautifulsoup4

# --- Config ---
LOGIN_URL = "https://rokomari.com/login"
IDENTIFIER = "mytestautomation11@gmail.com"
IMAP_HOST = "imap.gmail.com"
IMAP_USER = "mytestautomation11@gmail.com"
IMAP_PASS = "jlou okfw lgve qvdk"  # App Password
OTP_REGEX = r"\b\d{4,6}\b"  # OTP can be 4-6 digits
MAX_WAIT = 120  # wait up to 2 minutes
POLL_INTERVAL = 5

# --- Start browser ---
service = Service(r"F:\drivers\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service)
driver.get(LOGIN_URL)
driver.maximize_window()

# --- Step 1: Enter email and click NEXT ---
email_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.NAME, "username"))
)
email_input.clear()
email_input.send_keys(IDENTIFIER)

next_btn = driver.find_element(By.XPATH, '//*[@id="js--btn-next"]')
next_btn.click()
time.sleep(8)
# --- Step 2: Fetch OTP from email ---
def fetch_latest_otp(imap_host, user, password, regex):
    mail = imaplib.IMAP4_SSL(imap_host)
    mail.login(user, password)
    mail.select("inbox")

    end_time = time.time() + MAX_WAIT
    while time.time() < end_time:
        status, data = mail.search(None, 'ALL')  # check all emails
        if status != "OK":
            time.sleep(POLL_INTERVAL)
            continue

        mail_ids = data[0].split()
        if not mail_ids:
            time.sleep(POLL_INTERVAL)
            continue

        for mid in reversed(mail_ids):  # check latest first
            status, msg_data = mail.fetch(mid, "(RFC822)")
            if status != "OK":
                continue
            msg = email.message_from_bytes(msg_data[0][1])

            body = ""
            if msg.is_multipart():
                for part in msg.walk():
                    ctype = part.get_content_type()
                    if ctype in ["text/plain", "text/html"]:
                        payload = part.get_payload(decode=True)
                        if payload:
                            text = payload.decode(errors="ignore")
                            if ctype == "text/html":
                                text = BeautifulSoup(text, "html.parser").get_text()
                            body += text + "\n"
            else:
                body = msg.get_payload(decode=True).decode(errors="ignore")

            # Debug print
            print("Checking email ID:", mid.decode())
            print("Email body preview:\n", body[:200])

            m = re.search(regex, body)
            if m:
                return m.group(0)

        time.sleep(POLL_INTERVAL)

    return None

otp = fetch_latest_otp(IMAP_HOST, IMAP_USER, IMAP_PASS, OTP_REGEX)
if not otp:
    print("❌ OTP not found")
    driver.quit()
    raise SystemExit("No OTP received")

print("✅ Got OTP:", otp)

# --- Step 3: Enter OTP and verify ---
otp_input = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.XPATH, '//*[@id="otp-login-form"]/div[1]/div/input'))
)
otp_input.clear()
otp_input.send_keys(otp)
otp_input.send_keys(Keys.RETURN)  # Submit OTP

# --- Step 4: Confirm login successful ---
try:
    dashboard = WebDriverWait(driver, 15).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "div.dashboard"))
    )
    print("✅ Logged in successfully")
except Exception as e:
    print("⚠️ Login might have failed:", e)
