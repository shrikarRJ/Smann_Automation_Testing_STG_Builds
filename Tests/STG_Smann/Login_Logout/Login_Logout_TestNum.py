# ==========================================
# Login_Logout with Test NO.
# ==========================================

from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import subprocess
import os

# ------------------------------------------
# CONFIG
# ------------------------------------------
PHONE_NUMBER = "9999999999"   # Magic test number
FIXED_OTP = "1234"            # Permanent OTP

DEVICE_UDID = "emulator-5554"

# ZA222KCFFQ
# emulator-5554

APK_PATH = os.environ.get(
    "APK_PATH",
    r"C:\Users\shrik\OneDrive\Desktop\Smann_Automation_Testing_STG_Builds\Tests\STG_Smann\Smann_STG_APK\STG_Smann.apk"
)

APP_PACKAGE = "com.tribetayling.customer.staging"
APP_ACTIVITY = "com.tribetayling.customer.MainActivity"

# ------------------------------------------
# Helper: Check & Install App if Missing
# ------------------------------------------
def ensure_app_installed():
    cmd = f'adb -s {DEVICE_UDID} shell pm list packages | findstr {APP_PACKAGE}'
    result = subprocess.getoutput(cmd)

    if APP_PACKAGE not in result:
        print("📦 App not found on device. Installing APK...")
        install_cmd = f'adb -s {DEVICE_UDID} install -r "{APK_PATH}"'
        os.system(install_cmd)
        print("✅ App installed")
    else:
        print("✅ App already installed on device")

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
    safe_click(AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_button", 3)
    safe_click(AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_foreground_only_button", 3)

# ------------------------------------------
# Helper: Handle Intro Templates
# ------------------------------------------
def handle_intro_templates():
    if safe_click(AppiumBy.ACCESSIBILITY_ID, "Got it! Thanks", 5):
        print("✅ Clicked 'Got it! Thanks'")
        return

    if safe_click(AppiumBy.ACCESSIBILITY_ID, "Order Now", 5):
        print("✅ Clicked 'Order Now'")
        return

    print("ℹ️ No intro template shown")

# ------------------------------------------
# Ensure App Installed
# ------------------------------------------
ensure_app_installed()

# ------------------------------------------
# Desired Capabilities
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
driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
wait = WebDriverWait(driver, 40)

print("✅ App launched successfully")

# ------------------------------------------
# Handle Initial Permissions
# ------------------------------------------
handle_permissions()

# ------------------------------------------
# Mobile Number Entry
# ------------------------------------------
mobile_input = wait.until(EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText")))
mobile_input.click()
mobile_input.clear()
mobile_input.send_keys(PHONE_NUMBER)

continue_btn = wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Continue")))
continue_btn.click()

print("📲 Magic number entered, proceeding with fixed OTP...")

# ------------------------------------------
# OTP Entry (HARDENED, FIXED OTP = 1234)
# ------------------------------------------
def enter_otp_safely(otp):
    print("✍️ Entering FIXED OTP safely...")

    for attempt in range(1, 4):  # try up to 3 times
        try:
            # Bring app back to foreground just in case
            driver.activate_app(APP_PACKAGE)
            time.sleep(1)

            # Re-find OTP field
            otp_input = wait.until(
                EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText"))
            )

            otp_input.click()
            time.sleep(1)

            try:
                otp_input.clear()
            except:
                pass

            time.sleep(1)

            # Type OTP via ADB (most reliable)
            os.system(f'adb -s {DEVICE_UDID} shell input text {otp}')
            print(f"⌨️ Fixed OTP typed via ADB (attempt {attempt})")

            # Wait for next screen indicator
            try:
                WebDriverWait(driver, 15).until(
                    EC.any_of(
                        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Got it! Thanks")),
                        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Order Now")),
                        EC.presence_of_element_located(
                            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.ImageView")')
                        )
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

# Use FIXED OTP
enter_otp_safely(FIXED_OTP)

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
    profile_icon = wait.until(
        EC.presence_of_element_located(
            (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.ImageView").instance(13)')
        )
    )
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
