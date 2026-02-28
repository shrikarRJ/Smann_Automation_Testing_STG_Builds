# ==========================================
# Full Order Flow with Test NO. (9999999999) and Fixed OTP (1234) - COMPLETE VERSION
# Skip -> Select Address -> Add Items -> Cart -> Login -> Place Order -> Payment -> Success -> Logout
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
PHONE_NUMBER = "9999999999"
FIXED_OTP = "1234"

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
# def ensure_app_installed():
#     cmd = f'adb -s {DEVICE_UDID} shell pm list packages | findstr {APP_PACKAGE}'
#     result = subprocess.getoutput(cmd)

#     if APP_PACKAGE not in result:
#         print("📦 App not found on device. Installing APK...")
#         install_cmd = f'adb -s {DEVICE_UDID} install -r "{APK_PATH}"'
#         os.system(install_cmd)
#         print("✅ App installed")
#     else:
#         print("✅ App already installed on device")

# ------------------------------------------
# Helper: Safe click
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
# def handle_permissions():
#     safe_click(AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_button", 3)
#     safe_click(AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_foreground_only_button", 3)

# ------------------------------------------
# Helper: Handle Intro / Welcome Templates
# ------------------------------------------
# def handle_intro_templates():
#     if safe_click(AppiumBy.ACCESSIBILITY_ID, "Got it! Thanks", 3):
#         print("✅ Clicked 'Got it! Thanks'")
#         return
#     if safe_click(AppiumBy.ACCESSIBILITY_ID, "Order Now", 3):
#         print("✅ Clicked 'Order Now'")
#         return
#     if safe_click(AppiumBy.ACCESSIBILITY_ID, "Skip", 3):
#         print("✅ Clicked 'Skip'")
#         return

# ------------------------------------------
# Helper: Fill Complete Address SAFELY
# ------------------------------------------
# def fill_complete_address():
#     print("🏠 Filling complete address details...")

#     addr1 = wait.until(
#         EC.presence_of_element_located(
#             (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(0)')
#         )
#     )
#     addr1.click()
#     addr1.clear()
#     addr1.send_keys("Bus stand")
#     time.sleep(1)

#     addr2 = wait.until(
#         EC.presence_of_element_located(
#             (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(1)')
#         )
#     )
#     addr2.click()
#     addr2.clear()
#     addr2.send_keys("Khopoli")
#     time.sleep(1)

#     driver.execute_script('mobile:pressKey', {"keycode": 4})
#     time.sleep(1)

#     print("✅ Address fields filled, confirming address...")
#     safe_click(AppiumBy.ACCESSIBILITY_ID, "Confirm Address", 10)

# ------------------------------------------
# Helper: Click Cart Button (ANY "X items added") - STABLE
# ------------------------------------------
# def open_cart_from_items_added():
#     print("🛒 Waiting for cart button (X items added)...")

#     for attempt in range(1, 6):
#         try:
#             cart_btn = WebDriverWait(driver, 20).until(
#                 EC.element_to_be_clickable(
#                     (AppiumBy.ANDROID_UIAUTOMATOR,
#                      'new UiSelector().descriptionContains("items added")')
#                 )
#             )
#             cart_btn.click()
#             print(f"✅ Clicked cart button (attempt {attempt})")
#             time.sleep(2)
#             return True
#         except Exception as e:
#             print(f"⚠️ Cart button not stable yet (attempt {attempt}), retrying...")
#             time.sleep(2)

#     raise Exception("❌ Failed to click cart button with 'items added'")

# ------------------------------------------
# Helper: Enter OTP Safely (Fixed OTP)
# ------------------------------------------
# def enter_otp_safely(otp):
#     print("✍️ Entering FIXED OTP safely...")

#     for attempt in range(1, 4):
#         try:
#             driver.activate_app(APP_PACKAGE)
#             time.sleep(1)

#             otp_input = wait.until(
#                 EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText"))
#             )
#             otp_input.click()

#             try:
#                 otp_input.clear()
#             except:
#                 pass

#             os.system(f'adb -s {DEVICE_UDID} shell input text {otp}')
#             print(f"⌨️ Fixed OTP typed (attempt {attempt})")

#             time.sleep(4)
#             return True
#         except Exception as e:
#             print(f"⚠️ Error while entering OTP (attempt {attempt}): {e}")
#             time.sleep(2)

#     raise Exception("❌ Failed to enter OTP")

# ------------------------------------------
# START TEST
# ------------------------------------------
# ensure_app_installed()

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

driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
wait = WebDriverWait(driver, 40)

# print("✅ App launched successfully")

# handle_permissions()
# handle_intro_templates()

# ------------------------------------------
# Location Flow
# ------------------------------------------
# safe_click(AppiumBy.ACCESSIBILITY_ID, "Enter location manually", 10)

# search_box = wait.until(EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText")))
# search_box.click()
# search_box.clear()
# search_box.send_keys("khopoli bus stand")

# safe_click(
#     AppiumBy.ACCESSIBILITY_ID,
#     "Khopoli ST Stand, Khopoli ST Bus Stand, Laxminagar, Khopoli, Maharashtra, India",
#     15
# )

# safe_click(AppiumBy.ACCESSIBILITY_ID, "Add more address details", 10)
# fill_complete_address()

# ------------------------------------------
# Browse & Add Items
# ------------------------------------------
# safe_click(AppiumBy.ACCESSIBILITY_ID, "FOOD", 15)
# safe_click(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("King cafe")', 15)
# safe_click(AppiumBy.ACCESSIBILITY_ID, "Menu", 10)

# # Add 2 items (flexible)
# safe_click(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Add").instance(0)', 10)
# safe_click(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Add").instance(1)', 10)

# open_cart_from_items_added()

# ------------------------------------------
# Login Flow
# ------------------------------------------
# safe_click(AppiumBy.ACCESSIBILITY_ID, "LogIn", 10)

# mobile_input = wait.until(EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText")))
# mobile_input.click()
# mobile_input.clear()
# mobile_input.send_keys(PHONE_NUMBER)

# safe_click(AppiumBy.ACCESSIBILITY_ID, "Continue", 10)
# enter_otp_safely(FIXED_OTP)

# handle_permissions()
# handle_intro_templates()

# ------------------------------------------
# PLACE ORDER FLOW (from your recorded script)
# ------------------------------------------
# print("🧾 Proceeding to Place Order...")

safe_click(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Place Order")', 20)

# safe_click(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Apps & UPI ID")', 15)
# safe_click(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().textContains("Using as")', 15)
# safe_click(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.Button")', 15)
# safe_click(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Continue")', 15)

# Card screen / fallback screens
# safe_click(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Go back")', 10)

# Enter card details (as per your recorded flow)
safe_click(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.view.View")', 10)

card1 = wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(0)')))
card1.send_keys("4100280000001007")

card2 = wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(1)')))
card2.send_keys("0630")

card3 = wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(2)')))
card3.send_keys("630")

# driver.execute_script('mobile:pressKey', {"keycode": 4})

safe_click(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Continue")', 15)
safe_click(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Maybe later")', 10)
safe_click(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Success")', 20)

# ------------------------------------------
# Logout Flow
# ------------------------------------------
safe_click(AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.ImageView").instance(13)', 15)
safe_click(AppiumBy.ACCESSIBILITY_ID, "Sign out", 10)
safe_click(AppiumBy.ACCESSIBILITY_ID, "Sign Out", 10)

print("✅ Full flow completed successfully")

time.sleep(2)
driver.quit()
print("✅ Test execution finished")