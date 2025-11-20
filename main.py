import time
import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

import db_manager

def generate_new_password():
    prefix = "Tox"
    chars = string.ascii_lowercase + string.digits
    random_part = "".join(random.choices(chars, k=7))
    return f"{prefix}{random_part}"

def slow_type(element, text, delay=0.15):
    for char in text:
        element.send_keys(char)
        time.sleep(delay)

def change_password_and_logout(driver, username, current_password, new_password):
    wait = WebDriverWait(driver, 30)
    driver.get("https://unlocktool.net/post-in/")
    time.sleep(random.uniform(3, 5))

    try:
        user_input = wait.until(EC.presence_of_element_located((By.NAME, "username")))
        slow_type(user_input, username)
        pass_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
        slow_type(pass_input, current_password)

        print(f"🤖 Đang xử lý CAPTCHA cho {username}...")
        iframe = wait.until(EC.presence_of_element_located((By.XPATH, "//iframe[starts-with(@name, 'a-') and starts-with(@src, 'https://www.google.com/recaptcha')]")))
        driver.switch_to.frame(iframe)
        checkbox = wait.until(EC.element_to_be_clickable((By.ID, "recaptcha-anchor")))
        checkbox.click()
        driver.switch_to.default_content()
        time.sleep(random.uniform(5, 10))

        login_btn = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@type='submit' and contains(text(), 'Login')]")))
        login_btn.click()        
        wait.until(EC.presence_of_element_located((By.XPATH, "//a[contains(@href, '/logout/')]")))
        print(f"✅ {username} login thành công")

    except Exception as e:
        print(f"⚠️ Không thể login cho {username} (có thể đã login sẵn). Lỗi: {e}. Thử truy cập trực tiếp...")

    time.sleep(random.uniform(3, 5))
    driver.get("https://unlocktool.net/password-change/")

    wait.until(EC.presence_of_element_located((By.NAME, "old_password"))).send_keys(current_password)
    driver.find_element(By.NAME, "new_password1").send_keys(new_password)
    driver.find_element(By.NAME, "new_password2").send_keys(new_password)
    driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()    
    # Chờ thông báo thành công
    wait.until(EC.url_contains("/password-change/done"))
    print(f"🔁 {username} đã đổi mật khẩu thành {new_password}")

    time.sleep(random.uniform(2, 4))
    driver.get("https://unlocktool.net/logout")
    print(f"🚪 {username} đã logout")
    time.sleep(random.uniform(5, 8))

if __name__ == "__main__":
    accounts = db_manager.get_accounts_to_process()
    if not accounts:
        print("Không có tài khoản nào cần xử lý.")
    else:
        db_manager.lock_accounts_for_update([acc['_id'] for acc in accounts])

    options = Options()
    # Không chạy headless, không ẩn automation để bạn theo dõi quá trình
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--user-data-dir=C:\\Users\\PC\\selenium-profile")
    # Đường dẫn chrome.exe chuẩn cho Windows 10
    options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

    # === Kỹ thuật ẩn bot ===
    options.add_experimental_option("excludeSwitches", ["enable-automation"])    
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")

    driver = webdriver.Chrome(
        service=ChromeService(ChromeDriverManager().install()),
        options=options
    )

    # Ẩn navigator.webdriver
    driver.execute_cdp_cmd(
        "Page.addScriptToEvaluateOnNewDocument",
        {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"}
    )

    try:
        for acc in accounts:
            username = acc['username']
            current_password = acc['password']
            new_password = generate_new_password()
            try:
                change_password_and_logout(driver, username, current_password, new_password)
                db_manager.update_account_password(acc['_id'], new_password)
                print(f"✅ Đã cập nhật mật khẩu mới cho {username}")
            except Exception as e:
                print(f"❌ Lỗi nghiêm trọng tại {username}: {e}")
    finally:
        driver.quit()
        print("====== Job Finished ======")
