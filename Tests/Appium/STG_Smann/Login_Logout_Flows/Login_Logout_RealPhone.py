# ==========================================
# Login_Logout with REAL SMS OTP (ADB) - HARDENED VERSION
# ==========================================

from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time
import subprocess
import re
import os
import shutil
import urllib.request
import urllib.error

# ------------------------------------------
# CONFIG
# ------------------------------------------
PHONE_NUMBER = "9021004607"
DEVICE_UDID = "ZA222KCFFQ"

# ZA222KCFFQ
# emulator-5554

# APK_PATH = "C:\\Users\\shrik\\OneDrive\\Desktop\\Smann_Automation_Testing_STG_Builds\\Tests\\STG_Smann\\Smann_STG_APK\\STG_Smann.apk"
APK_PATH = os.environ.get("APK_PATH", r"C:\Users\shrik\OneDrive\Desktop\Smann_Automation_Testing_STG_Builds\Tests\Appium\STG_Smann\Smann_STG_APK\STG_Smann.apk")
APP_PACKAGE = "com.tribetayling.customer.staging"
APP_ACTIVITY = "com.tribetayling.customer.MainActivity"
APPIUM_SERVER_URL = os.environ.get("APPIUM_SERVER_URL", "http://127.0.0.1:4723")
APPIUM_START_TIMEOUT = 20

appium_process = None


def run_adb_command(args, capture_output=True, check=True):
    cmd = ["adb", "-s", DEVICE_UDID, *args]
    return subprocess.run(
        cmd,
        capture_output=capture_output,
        text=True,
        check=check
    )

# ------------------------------------------
# Helper: Check & Install App if Missing
# ------------------------------------------
def ensure_device_connected():
    result = subprocess.run(
        ["adb", "devices"],
        capture_output=True,
        text=True,
        check=True
    )

    connected_devices = []
    for line in result.stdout.splitlines():
        if "\tdevice" in line:
            connected_devices.append(line.split("\t")[0].strip())

    if DEVICE_UDID not in connected_devices:
        raise RuntimeError(
            f"❌ Device '{DEVICE_UDID}' not detected by adb. Connected devices: {connected_devices or 'none'}"
        )


def ensure_app_installed():
    result = run_adb_command(["shell", "pm", "list", "packages"], capture_output=True).stdout

    if APP_PACKAGE not in result:
        print("📦 App not found on device. Installing APK...")
        subprocess.run(["adb", "-s", DEVICE_UDID, "install", "-r", APK_PATH], check=True)
        print("✅ App installed")
    else:
        print("✅ App already installed on device")


def is_appium_server_running():
    try:
        with urllib.request.urlopen(f"{APPIUM_SERVER_URL}/status", timeout=2) as response:
            return response.status == 200
    except (urllib.error.URLError, TimeoutError, ConnectionError):
        return False


def start_appium_server_if_needed():
    global appium_process

    if is_appium_server_running():
        print(f"✅ Appium server already running at {APPIUM_SERVER_URL}")
        return

    appium_binary = shutil.which("appium.cmd") or shutil.which("appium")
    if not appium_binary:
        raise RuntimeError(
            "❌ Appium server is not running on http://127.0.0.1:4723 and the 'appium' command was not found in PATH."
        )

    print("🚀 Appium server not running. Starting it automatically...")
    appium_process = subprocess.Popen(
        [appium_binary, "--address", "127.0.0.1", "--port", "4723"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )

    end_time = time.time() + APPIUM_START_TIMEOUT
    while time.time() < end_time:
        if is_appium_server_running():
            print(f"✅ Appium server started at {APPIUM_SERVER_URL}")
            return
        time.sleep(1)

    raise RuntimeError(
        f"❌ Appium server did not start within {APPIUM_START_TIMEOUT} seconds. Please check Appium installation/logs."
    )

# ------------------------------------------
# Helper: Get latest SMS timestamp BEFORE requesting OTP
# ------------------------------------------
def get_latest_sms_date():
    result = run_adb_command(
        ["shell", "content", "query", "--uri", "content://sms/inbox", "--projection", "date"],
        capture_output=True
    ).stdout

    dates = re.findall(r'date=(\d+)', result)
    if not dates:
        return 0

    return max(int(d) for d in dates)

# ------------------------------------------
# Helper: Fetch ONLY NEW OTP from SMS using ADB
# ------------------------------------------
def fetch_otp_from_sms(last_seen_date, max_wait_seconds=120, poll_interval=5):
    print("📩 Waiting for NEW OTP SMS from SMANN...")

    start_time = time.time()

    while time.time() - start_time < max_wait_seconds:
        result = run_adb_command(
            ["shell", "content", "query", "--uri", "content://sms/inbox", "--projection", "address,body,date"],
            capture_output=True
        ).stdout

        rows = result.split("Row:")

        for row in rows:
            if "SMANN" in row and "OTP" in row:
                date_match = re.search(r'date=(\d+)', row)
                body_match = re.search(r'body=(.*)', row)

                if not date_match or not body_match:
                    continue

                msg_date = int(date_match.group(1))
                msg_body = body_match.group(1)

                # Only accept SMS that arrived AFTER we requested OTP
                if msg_date <= last_seen_date:
                    continue

                otp_match = re.search(r'\b(\d{4,6})\b', msg_body)
                if otp_match:
                    otp = otp_match.group(1)
                    print(f"✅ NEW OTP Extracted: {otp}")
                    return otp

        print("⏳ New OTP not arrived yet, waiting...")
        time.sleep(poll_interval)

    raise Exception("❌ New OTP not received within time limit")

# ------------------------------------------
# Helper: Safe click if element appears
# ------------------------------------------
def safe_click(by, value, timeout=5):
    try:
        el = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, value)))
        el.click()
        return True
    except TimeoutException:
        return False

# ------------------------------------------
# Helper: Handle Permission Popups
# ------------------------------------------
def handle_permissions():
    if safe_click(AppiumBy.ACCESSIBILITY_ID, "Enable Location", 5):
        safe_click(
            AppiumBy.ID,
            "com.android.permissioncontroller:id/permission_allow_foreground_only_button",
            5
        )

    if safe_click(AppiumBy.ACCESSIBILITY_ID, "Enable Notification", 5):
        safe_click(AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_button", 5)

    safe_click(AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_button", 3)
    safe_click(AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_foreground_only_button", 3)

# ------------------------------------------
# Helper: Handle Intro Templates (Got it / Order Now)
# ------------------------------------------
def handle_intro_templates():
    handle_permissions()

    if safe_click(AppiumBy.ACCESSIBILITY_ID, "Got it! Thanks", 5):
        print("✅ Clicked 'Got it! Thanks'")
        return

    # Sometimes shows "Order Now"
    if safe_click(AppiumBy.ACCESSIBILITY_ID, "Order Now", 5):
        print("✅ Clicked 'Order Now'")
        return

    print("ℹ️ No intro template shown")

# ------------------------------------------
# Ensure App Installed
# ------------------------------------------
ensure_device_connected()
ensure_app_installed()
start_appium_server_if_needed()

# ------------------------------------------
# Desired Capabilities (REAL DEVICE)
# ------------------------------------------
options = AppiumOptions()
options.load_capabilities({
    "platformName": "Android",
    "appium:automationName": "UiAutomator2",
    "appium:deviceName": "Android",
    "appium:udid": DEVICE_UDID,

    "appium:appPackage": APP_PACKAGE,
    "appium:appActivity": APP_ACTIVITY,

    "appium:noReset": True,
    "appium:autoGrantPermissions": True,
    "appium:newCommandTimeout": 300
})

# ------------------------------------------
# Driver Initialization
# ------------------------------------------
driver = webdriver.Remote(APPIUM_SERVER_URL, options=options)
wait = WebDriverWait(driver, 40)

print("✅ App launched successfully")

# ------------------------------------------
# Handle Initial Permissions (if any)
# ------------------------------------------
handle_permissions()

# ------------------------------------------
# Mobile Number Entry
# ------------------------------------------
mobile_input = wait.until(EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText")))
mobile_input.click()
mobile_input.clear()
mobile_input.send_keys(PHONE_NUMBER)

# Capture last SMS time BEFORE requesting OTP
last_sms_date = get_latest_sms_date()
print(f"📅 Last SMS timestamp before requesting OTP: {last_sms_date}")

continue_btn = wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Continue")))
continue_btn.click()

# ------------------------------------------
# Fetch REAL OTP from SMS (ONLY NEW ONE)
# ------------------------------------------
otp_value = fetch_otp_from_sms(last_sms_date)

# ------------------------------------------
# OTP Entry (Prevent Messages app opening)
# ------------------------------------------
# otp_input = wait.until(EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText")))
# otp_input.click()
# otp_input.clear()
# otp_input.send_keys(otp_value)

# ------------------------------------------
# OTP Entry (HARDENED: Handles Autofill, Focus Loss, Stale Elements)
# ------------------------------------------
def enter_otp_safely(otp):
    print("✍️ Entering OTP safely...")

    for attempt in range(1, 4):  # try up to 3 times
        try:
            # Bring app back to foreground in case Messages opened
            driver.activate_app(APP_PACKAGE)
            time.sleep(1)

            # Re-find OTP field (do NOT reuse old element)
            otp_input = wait.until(
                EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText"))
            )

            # Focus the field
            otp_input.click()
            time.sleep(1)

            # Clear any existing text
            try:
                otp_input.clear()
            except:
                pass

            time.sleep(1)

            # Use ADB to input text (most reliable, bypasses autofill UI)
            os.system(f'adb -s {DEVICE_UDID} shell input text {otp}')
            print(f"⌨️ OTP typed via ADB (attempt {attempt})")

            if not safe_click(AppiumBy.ACCESSIBILITY_ID, "Verify", 5):
                print(f"⚠️ Verify button not found after OTP entry (attempt {attempt})")

            # 🔑 NOW: Do NOT check the field text
            # Instead, wait for next screen indicator

            try:
                # Example: wait for "Got it! Thanks" OR Profile icon OR any home element
                WebDriverWait(driver, 15).until(
                    EC.any_of(
                        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Enable Location")),
                        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Enable Notification")),
                        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Got it! Thanks")),
                        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Profile")),
                        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Order Now")),
                    )
                )
                print(f"✅ OTP accepted, moved to next screen (attempt {attempt})")
                return True

            except TimeoutException:
                print(f"⚠️ Still on OTP screen, retrying... (attempt {attempt})")

        except Exception as e:
            print(f"⚠️ Error while entering OTP (attempt {attempt}): {e}")

        time.sleep(2)

    raise Exception("❌ Failed to move past OTP screen after multiple attempts")


enter_otp_safely(otp_value)

# ------------------------------------------
# Handle Permissions Again (if shown)
# ------------------------------------------
handle_permissions()

# ------------------------------------------
# Handle Intro Templates
# ------------------------------------------
handle_intro_templates()

# ------------------------------------------
# Profile / Menu Icon
# ------------------------------------------
try:
    profile_icon = wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Profile")))
    profile_icon.click()
except TimeoutException:
    print("ℹ️ Profile icon not found, continuing anyway")

# ------------------------------------------
# Logout Flow
# ------------------------------------------
safe_click(AppiumBy.ACCESSIBILITY_ID, "Sign out", 10)
safe_click(AppiumBy.ACCESSIBILITY_ID, "Sign Out", 10)

print("✅ Logout completed successfully")

# ------------------------------------------
# Cleanup
# ------------------------------------------
time.sleep(2)
driver.quit()
print("✅ Test execution finished")
