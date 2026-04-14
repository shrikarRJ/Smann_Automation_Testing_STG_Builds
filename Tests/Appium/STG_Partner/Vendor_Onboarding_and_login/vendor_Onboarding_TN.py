# ==========================================
# STG_Vendor_Onboarding_And_Logout (FULL STABLE + COORD SCROLL)
# ==========================================

from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

import time
import subprocess
import os

# ------------------------------------------
# CONFIG
# ------------------------------------------
UNIQUE_CODE = "0121"
BASE_PHONE = "999999"
FIXED_OTP = "1234"

PHONE_NUMBER = BASE_PHONE + UNIQUE_CODE
SHOP_NAME = f"{UNIQUE_CODE} Shop Name"
BUILDING_NAME = f"{UNIQUE_CODE} building name"
LANDMARK_TEXT = "near railway station"

DEVICE_UDID = "emulator-5554"

APK_PATH = r"C:\Users\shrik\OneDrive\Desktop\Smann_Automation_Testing_STG_Builds\Tests\STG_Partner\STG_Partner_Apk\STG_Partner.apk"

APP_PACKAGE = "com.tribetayling.vendor.staging"
APP_ACTIVITY = "com.tribetayling.vendor.MainActivity"

# ------------------------------------------
# ADB TYPE (RELIABLE, NO MISSING FIRST LETTER)
# ------------------------------------------
def adb_type_fast(text):
    os.system(f'adb -s {DEVICE_UDID} shell input text "{text.replace(" ", "%s")}"')
    time.sleep(0.4)

def adb_back():
    os.system(f'adb -s {DEVICE_UDID} shell input keyevent 4')
    time.sleep(0.3)

# ------------------------------------------
# SAFE FIND / CLICK
# ------------------------------------------
def safe_find(by, value, timeout=20):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )

def safe_click(by, value, timeout=20):
    el = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, value))
    )
    el.click()
    time.sleep(0.6)

# ------------------------------------------
# SCROLL HELPERS
# ------------------------------------------
def swipe_up():
    size = driver.get_window_size()
    x = size["width"] // 2
    start_y = int(size["height"] * 0.75)
    end_y = int(size["height"] * 0.25)
    driver.swipe(x, start_y, x, end_y, 800)
    time.sleep(1)

def swipe_horizontal_by_coords(x1, y1, x2, y2, duration=0.1):
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(x1, y1)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.pause(duration)
    actions.w3c_actions.pointer_action.move_to_location(x2, y2)
    actions.w3c_actions.pointer_action.release()
    actions.perform()
    time.sleep(1)

def tap_by_coords(x, y):
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(x, y)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.pause(0.1)
    actions.w3c_actions.pointer_action.release()
    actions.perform()
    time.sleep(0.6)

def optional_click(by, value, wait_seconds=3):
    try:
        el = WebDriverWait(driver, wait_seconds).until(
            EC.element_to_be_clickable((by, value))
        )
        el.click()
        print(f"✅ Optional popup clicked: {value}")
        return True
    except TimeoutException:
        print(f"ℹ️ Optional popup not shown: {value} (continuing)")
        return False

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
    "appium:deviceName": "Android",
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

safe_click(AppiumBy.CLASS_NAME, "android.widget.CheckBox")
adb_back()
safe_click(AppiumBy.ACCESSIBILITY_ID, "Get OTP")
print(f"📲 Phone entered: {PHONE_NUMBER}")

# ------------------------------------------
# OTP
# ------------------------------------------
otp_input = safe_find(AppiumBy.CLASS_NAME, "android.widget.EditText")
otp_input.click()
adb_type_fast(FIXED_OTP)
print("✅ OTP entered")

# ------------------------------------------
# Address Search
# ------------------------------------------
search_box = safe_find(
    AppiumBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().className("android.widget.EditText").instance(0)'
)
search_box.click()
adb_type_fast("railway station khopoli")

safe_click(
    AppiumBy.ACCESSIBILITY_ID,
    "Railway Station Road, Indira Nagar, Laxminagar, Khopoli, Maharashtra, India"
)
print("📍 Address selected")

# ------------------------------------------
# Add Address Screen
# ------------------------------------------
safe_find(AppiumBy.ACCESSIBILITY_ID, "Use Current Location")
print("✅ On Add Address screen")

# Flat / Shop No
flat_field = safe_find(
    AppiumBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().className("android.widget.EditText").instance(1)'
)
flat_field.click()
adb_type_fast(UNIQUE_CODE)
adb_back()

# Building Name
building_field = safe_find(
    AppiumBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().className("android.widget.EditText").instance(2)'
)
building_field.click()
adb_type_fast(BUILDING_NAME)
adb_back()

# Landmark
swipe_up()
safe_click(AppiumBy.ACCESSIBILITY_ID, "Enter landmark")

landmark_input = safe_find(
    AppiumBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().className("android.widget.EditText").instance(1)'
)
landmark_input.click()
adb_type_fast(LANDMARK_TEXT)
adb_back()

print("📍 Landmark entered")

# Save
swipe_up()
safe_click(AppiumBy.ACCESSIBILITY_ID, "Save")
print("✅ Address saved")

# ------------------------------------------
# WAIT FOR SHOP DETAILS SCREEN (IMPORTANT)
# ------------------------------------------
print("⏳ Waiting for Shop Details screen...")

shop_field = WebDriverWait(driver, 40).until(
    EC.presence_of_element_located(
        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(0)')
    )
)

time.sleep(1)
shop_field.click()
adb_type_fast(SHOP_NAME)
adb_back()
print(f"🏪 Shop name entered: {SHOP_NAME}")

# ------------------------------------------
# Categories (COORDINATE BASED HORIZONTAL SCROLL + TAP OTHERS)
# ------------------------------------------
print("➡️ Scrolling horizontally to reach 'Others' category...")

# These are from your recorded script gestures
swipe_horizontal_by_coords(642, 1851, 38, 1847)
swipe_horizontal_by_coords(909, 1851, 104, 1843)
swipe_horizontal_by_coords(875, 1830, 142, 1838)

print("👉 Tapping on 'Others' category...")

tap_by_coords(775, 1838)

print("✅ Clicked 'Others' category")

# Scroll down for next options
swipe_up()
swipe_up()

# ------------------------------------------
# Delivery & Payment
# ------------------------------------------
safe_click(AppiumBy.ACCESSIBILITY_ID, "Delivery")
safe_click(AppiumBy.ACCESSIBILITY_ID, "Online")
safe_click(AppiumBy.ACCESSIBILITY_ID, "Cash")

safe_click(AppiumBy.ACCESSIBILITY_ID, "Submit")
safe_click(AppiumBy.ACCESSIBILITY_ID, "Submit")

print("✅ Shop setup submitted")

# ------------------------------------------
# Skips, Inventory, Logout
# ------------------------------------------
safe_click(AppiumBy.ACCESSIBILITY_ID, "Skip")
safe_click(AppiumBy.ACCESSIBILITY_ID, "Skip")
safe_click(AppiumBy.ACCESSIBILITY_ID, "Skip")
safe_click(AppiumBy.ACCESSIBILITY_ID, "Skip")
safe_click(AppiumBy.ACCESSIBILITY_ID, "Skip for now")

safe_click(AppiumBy.ACCESSIBILITY_ID, "Create Inventory")

home_logo = safe_find(
    AppiumBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().description("Acme Logo").instance(1)',
    timeout=30
)
home_logo.click()
time.sleep(1)
print("🏠 Redirected to Home via Acme Logo")

safe_click(AppiumBy.ACCESSIBILITY_ID, "Skip")

# safe_click(AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_foreground_only_button")

optional_click(
    AppiumBy.ID,
    "com.android.permissioncontroller:id/permission_allow_foreground_only_button",
    wait_seconds=3
)

safe_click(AppiumBy.ACCESSIBILITY_ID, "Skip")
safe_click(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(32)')

swipe_up()
swipe_up()

safe_click(AppiumBy.ACCESSIBILITY_ID, "Sign out")
safe_click(AppiumBy.ACCESSIBILITY_ID, "Sign Out")

print("✅ Logout done")

time.sleep(2)
driver.quit()
print("✅ Test execution finished")