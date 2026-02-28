# ==========================================
# Wallet_Add_money.py (STABLE + OPTIONAL POPUPS + FIXED OTP)
# ==========================================

from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException

# For W3C actions (for coordinate taps)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

import time
import os
import subprocess

# ------------------------------------------
# CONFIG
# ------------------------------------------
DEVICE_UDID = "emulator-5554"

PHONE_NUMBER = "9999990108"
FIXED_OTP = "1234"

APK_PATH = os.environ.get(
    "APK_PATH",
    r"C:\Users\shrik\OneDrive\Desktop\Smann_Automation_Testing_STG_Builds\Tests\STG_Partner\STG_Partner_Apk\STG_Partner.apk"
)
APP_PACKAGE = "com.tribetayling.vendor.staging"
APP_ACTIVITY = "com.tribetayling.vendor.MainActivity"

# ------------------------------------------
# ADB FAST TYPE (NO MISSING CHARS)
# ------------------------------------------
def adb_type_fast(text):
    safe = text.replace(" ", "%s")
    os.system(f'adb -s {DEVICE_UDID} shell input text "{safe}"')
    time.sleep(0.4)

def adb_back():
    os.system(f'adb -s {DEVICE_UDID} shell input keyevent 4')
    time.sleep(0.4)

# ------------------------------------------
# SAFE HELPERS
# ------------------------------------------
def swipe_up():
    size = driver.get_window_size()
    x = size["width"] // 2
    start_y = int(size["height"] * 0.75)
    end_y = int(size["height"] * 0.25)
    driver.swipe(x, start_y, x, end_y, 800)
    time.sleep(1)

def safe_find(by, value, timeout=30):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )

def safe_click(by, value, timeout=30):
    el = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, value))
    )
    el.click()
    time.sleep(0.5)

def optional_click(by, value, wait_seconds=3):
    try:
        el = WebDriverWait(driver, wait_seconds).until(
            EC.element_to_be_clickable((by, value))
        )
        el.click()
        print(f"✅ Optional clicked: {value}")
        time.sleep(0.5)
        return True
    except TimeoutException:
        print(f"ℹ️ Optional not shown: {value} (continuing)")
        return False

# ------------------------------------------
# COORDINATE TAP HELPER
# ------------------------------------------
# def tap_xy(x, y):
#     actions = ActionChains(driver)
#     actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
#     actions.w3c_actions.pointer_action.move_to_location(x, y)
#     actions.w3c_actions.pointer_action.pointer_down()
#     actions.w3c_actions.pointer_action.pause(0.1)
#     actions.w3c_actions.pointer_action.release()
#     actions.perform()
#     time.sleep(0.5)

def tap_xy(x, y):
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(x, y)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.pause(0.1)
    actions.w3c_actions.pointer_action.release()
    actions.perform()
    time.sleep(0.5)

def safe_click(by, value, timeout=20, retries=3):
    for _ in range(retries):
        try:
            el = WebDriverWait(driver, timeout).until(
                EC.element_to_be_clickable((by, value))
            )
            el.click()
            time.sleep(0.5)
            return
        except (TimeoutException, StaleElementReferenceException):
            time.sleep(1)
    raise Exception(f"❌ Could not click: {value}")
# ------------------------------------------
# INSTALL CHECK
# ------------------------------------------
def ensure_app_installed():
    cmd = f'adb -s {DEVICE_UDID} shell pm list packages | findstr {APP_PACKAGE}'
    result = subprocess.getoutput(cmd)
    if APP_PACKAGE not in result:
        print("📦 Installing APK...")
        os.system(f'adb -s {DEVICE_UDID} install -r "{APK_PATH}"')
        print("✅ App installed")
    else:
        print("✅ App already installed")

# ------------------------------------------
# START
# ------------------------------------------
ensure_app_installed()

options = AppiumOptions()
options.load_capabilities({
    "platformName": "Android",
    "appium:automationName": "UiAutomator2",
    "appium:deviceName": DEVICE_UDID,
    "appium:udid": DEVICE_UDID,
    "appium:appPackage": APP_PACKAGE,
    "appium:appActivity": APP_ACTIVITY,
    "appium:noReset": False,
    "appium:autoGrantPermissions": True,
    "appium:newCommandTimeout": 300
})

driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
wait = WebDriverWait(driver, 40)

print("✅ App launched")

# ------------------------------------------
# Initial Screens
# ------------------------------------------
safe_click(AppiumBy.CLASS_NAME, "android.widget.Button")
safe_click(AppiumBy.CLASS_NAME, "android.widget.Button")
safe_click(AppiumBy.ACCESSIBILITY_ID, "Get started")
print("✅ Passed initial screens")

# ------------------------------------------
# Phone Number
# ------------------------------------------
phone_input = safe_find(AppiumBy.CLASS_NAME, "android.widget.EditText")
phone_input.click()
adb_type_fast(PHONE_NUMBER)

adb_back()
safe_click(AppiumBy.CLASS_NAME, "android.widget.CheckBox")
safe_click(AppiumBy.ACCESSIBILITY_ID, "Get OTP")

print(f"📲 Phone entered: {PHONE_NUMBER}")

# ------------------------------------------
# OTP (ALWAYS 1234)
# ------------------------------------------
otp_input = safe_find(AppiumBy.CLASS_NAME, "android.widget.EditText")
otp_input.click()
adb_type_fast(FIXED_OTP)

print("✅ OTP entered")

# ------------------------------------------
# OPTIONAL PERMISSION POPUP
# ------------------------------------------
optional_click(AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_foreground_only_button", 3)

# ------------------------------------------
# OPTIONAL SKIP
# ------------------------------------------
optional_click(AppiumBy.ACCESSIBILITY_ID, "Skip", 3)

# ------------------------------------------
# Open Menu (as per your recording)
# ------------------------------------------
safe_click(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(32)')

# ------------------------------------------
# Wallet
# ------------------------------------------
safe_click(AppiumBy.ACCESSIBILITY_ID, "Wallet")
safe_click(AppiumBy.ACCESSIBILITY_ID, "₹500")

# Tap Add / Continue area (recorded coordinate)
# print("💳 Selecting Cards payment method...")

# Tap on "Cards" using recorded coordinates
# tap_xy(959, 650)

# time.sleep(1)

# ------------------------------------------
# Card Details
# ------------------------------------------
# card_number = safe_find(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(0)')
# card_number.click()
# adb_type_fast("4100280000001007")

# expiry = safe_find(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(1)')
# expiry.click()
# adb_type_fast("1045")

# cvv = safe_find(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(2)')
# cvv.click()
# adb_type_fast("145")

# safe_click(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Continue")')

# ------------------------------------------
# Maybe later / Success (Optional screens)
# ------------------------------------------
# optional_click(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Maybe later")', 5)
# optional_click(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Success")', 5)

# ------------------------------------------
# Close success / back
# ------------------------------------------
# safe_click(AppiumBy.CLASS_NAME, "android.widget.Button")
# el19 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.Button")
# el19.click()
# print("💳 Selecting bank / card option...")


safe_click(
    AppiumBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().className("android.widget.Image").instance(5)',
    timeout=20
)

# Click "Axis Axis"
safe_click(
    AppiumBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().text("Axis Axis")',
    timeout=20
)

print("⏳ Waiting for payment success screen...")

# Click "Success"
safe_click(
    AppiumBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().text("Success")',
    timeout=30
)

print("✅ Payment success flow completed")

# Back button click:
print("⏳ Waiting before clicking Button...")
time.sleep(15)  # small buffer for UI animation

el1 = WebDriverWait(driver, 20).until(
    EC.element_to_be_clickable((AppiumBy.CLASS_NAME, "android.widget.Button"))
)
el1.click()
print("✅ Button clicked")



# Some swipe gestures from recording
swipe_up()
swipe_up()

# ------------------------------------------
# Logout
# ------------------------------------------
safe_click(AppiumBy.ACCESSIBILITY_ID, "Sign out")
safe_click(AppiumBy.ACCESSIBILITY_ID, "Sign Out")

print("✅ Logout done")

time.sleep(2)
driver.quit()
print("✅ Test execution finished")