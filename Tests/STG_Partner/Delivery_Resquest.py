import os
import time
import subprocess

from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# For W3C actions (coordinates)
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

# ------------------------------------------
# CONFIG
# ------------------------------------------
DEVICE_UDID = "emulator-5554"

# APK_PATH = r"C:\Users\shrik\OneDrive\Desktop\Smann_Automation_Testing_STG_Builds\Tests\STG_Partner\STG_Partner_Apk\STG_Partner.apk"
APK_PATH = os.environ.get(
    "APK_PATH",
    r"C:\Users\shrik\OneDrive\Desktop\Smann_Automation_Testing_STG_Builds\Tests\STG_Partner\STG_Partner_Apk\STG_Partner.apk"
)

APP_PACKAGE = "com.tribetayling.vendor.staging"
APP_ACTIVITY = "com.tribetayling.vendor.MainActivity"

BASE_PHONE = "999999"
UNIQUE_CODE = "0119"
PHONE_NUMBER = BASE_PHONE + UNIQUE_CODE

OTP_CODE = "1234"  # ALWAYS 1234

CUSTOMER_PHONE = "9000000001"
CUSTOMER_NAME = f"{UNIQUE_CODE} DR Test"
BUILDING_NO = UNIQUE_CODE
BUILDING_NAME = f"{UNIQUE_CODE} building name"

# ------------------------------------------
# HELPERS
# ------------------------------------------
def ensure_app_installed():
    print("🔍 Checking if app is installed...")
    cmd = f'adb -s {DEVICE_UDID} shell pm list packages | findstr {APP_PACKAGE}'
    result = subprocess.getoutput(cmd)

    if APP_PACKAGE not in result:
        print("📦 App not found. Installing APK...")
        os.system(f'adb -s {DEVICE_UDID} install -r "{APK_PATH}"')
        print("✅ App installed")
    else:
        print("✅ App already installed")


def safe_click(by, value, timeout=20):
    el = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, value))
    )
    el.click()
    time.sleep(0.5)

def adb_type_fast(text):
    os.system(f'adb -s {DEVICE_UDID} shell input text "{text.replace(" ", "%s")}"')
    time.sleep(0.4)


def safe_find(by, value, timeout=20):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )


def try_click(by, value, timeout=5):
    try:
        el = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        el.click()
        time.sleep(0.5)
        print(f"ℹ️ Clicked optional: {value}")
        return True
    except TimeoutException:
        print(f"ℹ️ Optional not present, skipping: {value}")
        return False
    
def swipe_up():
    size = driver.get_window_size()
    x = size["width"] // 2
    start_y = int(size["height"] * 0.75)
    end_y = int(size["height"] * 0.25)
    driver.swipe(x, start_y, x, end_y, 800)
    time.sleep(1)

def tap(x, y, pause=0.1):
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(x, y)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.pause(pause)
    actions.w3c_actions.pointer_action.release()
    actions.perform()
    time.sleep(0.5)


# def swipe(start_x, start_y, end_x, end_y):
#     actions = ActionChains(driver)
#     actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
#     actions.w3c_actions.pointer_action.move_to_location(start_x, start_y)
#     actions.w3c_actions.pointer_action.pointer_down()
#     actions.w3c_actions.pointer_action.move_to_location(end_x, end_y)
#     actions.w3c_actions.pointer_action.release()
#     actions.perform()
#     time.sleep(1)


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

print("🚀 App launched")

# ------------------------------------------
# Initial Screens
# ------------------------------------------
safe_click(AppiumBy.CLASS_NAME, "android.widget.Button")
safe_click(AppiumBy.CLASS_NAME, "android.widget.Button")
safe_click(AppiumBy.ACCESSIBILITY_ID, "Get started")
print("✅ Passed intro screens")

# ------------------------------------------
# Login
# ------------------------------------------
phone_input = safe_find(AppiumBy.CLASS_NAME, "android.widget.EditText")
phone_input.click()
phone_input.send_keys(PHONE_NUMBER)
driver.execute_script('mobile:pressKey', {"keycode": 4})

safe_click(AppiumBy.CLASS_NAME, "android.widget.CheckBox")
safe_click(AppiumBy.ACCESSIBILITY_ID, "Get OTP")
print(f"📲 Phone entered: {PHONE_NUMBER}")

otp_input = safe_find(AppiumBy.CLASS_NAME, "android.widget.EditText")
otp_input.click()
otp_input.send_keys(OTP_CODE)
print("✅ OTP entered (1234)")

# Skip if appears
try_click(AppiumBy.ACCESSIBILITY_ID, "Skip", timeout=5)

# ------------------------------------------
# Quick Delivery
# ------------------------------------------
safe_click(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Book a quick delivery")')
print("📦 Opened Quick Delivery")

cust_phone = safe_find(AppiumBy.CLASS_NAME, "android.widget.EditText")
cust_phone.click()
cust_phone.send_keys(CUSTOMER_PHONE)

time.sleep(3)

name_field = safe_find(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(0)')
name_field.click()
name_field.send_keys(CUSTOMER_NAME)
driver.execute_script('mobile:pressKey', {"keycode": 4})

safe_click(AppiumBy.ACCESSIBILITY_ID, "Select Drop Location*")


search_box = safe_find(
    AppiumBy.ANDROID_UIAUTOMATOR,
    'new UiSelector().className("android.widget.EditText").instance(0)'
)
search_box.click()
adb_type_fast("railway station khopoli")

print("⏳ Waiting before clicking address...")
time.sleep(3)

safe_click(
    AppiumBy.ACCESSIBILITY_ID,
    "Railway Station Road, Indira Nagar, Laxminagar, Khopoli, Maharashtra, India"
)
print("📍 Address selected")

print("⏳ Waiting before clicking Confirm Location Button...")
time.sleep(2)

safe_click(AppiumBy.ACCESSIBILITY_ID, "Confirm Location")

# Address fields
addr1 = safe_find(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(0)')
addr1.click()
addr1.send_keys(BUILDING_NO)

addr2 = safe_find(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(1)')
addr2.click()
addr2.send_keys(BUILDING_NAME)
driver.execute_script('mobile:pressKey', {"keycode": 4})

safe_click(AppiumBy.ACCESSIBILITY_ID, "Confirm Address")
print("📍 Address confirmed")
time.sleep(2)

# Scrolls (as recorded)
# swipe(529, 1747, 542, 792)
# swipe(429, 1747, 496, 384)
swipe_up()
swipe_up()
time.sleep(3)

# ------------------------------------------
# Book & Pay
# ------------------------------------------
safe_click(AppiumBy.ACCESSIBILITY_ID, "Book Delivery & Pay")
print("💳 Proceeding to payment")

# time.sleep(15)

# # Click Cards (image instance(6))
# safe_click(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.Image").instance(6)')

# # Select Bank
# safe_click(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Axis Axis")')

# # Success
# safe_click(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Success")')
# print("✅ Payment success")

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

try_click(AppiumBy.ACCESSIBILITY_ID, "Skip", timeout=5)

safe_click(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Book a quick delivery")')
print("📦 Opened Quick Delivery")

print("⏳ Waiting for 'View Delivery Requests' card to appear...")

# 1) Wait for the card by description and click it
el1 = WebDriverWait(driver, 30).until(
    EC.element_to_be_clickable((
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().description("View Delivery Requests\nTrack and manage all your delivery requests")'
    ))
)
el1.click()
print("✅ Clicked 'View Delivery Requests' card")

# Small wait for transition animation
time.sleep(1.5)

# 2) Coordinate tap (as per your recording)
print("⏳ Performing coordinate tap...")

actions = ActionChains(driver)
actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
actions.w3c_actions.pointer_action.move_to_location(513, 517)
actions.w3c_actions.pointer_action.pointer_down()
actions.w3c_actions.pointer_action.pause(0.15)  # slightly longer press = more reliable
actions.w3c_actions.pointer_action.release()
actions.perform()

print("✅ Coordinate tap performed")

# Back tap (coordinate)
# tap(492, 225)

safe_click(AppiumBy.ACCESSIBILITY_ID, "Back")
safe_click(AppiumBy.ACCESSIBILITY_ID, "Back")

# Open menu
safe_click(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View").instance(14)')

# Scroll menu
# swipe(388, 1618, 517, 438)
swipe_up()
swipe_up()

# Logout
safe_click(AppiumBy.ACCESSIBILITY_ID, "Sign out")
safe_click(AppiumBy.ACCESSIBILITY_ID, "Sign Out")
print("🚪 Logged out")

# ------------------------------------------
# END
# ------------------------------------------
time.sleep(2)
driver.quit()
print("🏁 Test execution finished successfully")