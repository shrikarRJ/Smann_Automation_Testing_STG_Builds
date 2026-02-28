# # This sample code supports Appium Python client >=2.3.0
# # pip install Appium-Python-Client
# # Then you can paste this into a file and simply run with Python

# from appium import webdriver
# from appium.options.common.base import AppiumOptions
# from appium.webdriver.common.appiumby import AppiumBy

# # For W3C actions
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.common.actions import interaction
# from selenium.webdriver.common.actions.action_builder import ActionBuilder
# from selenium.webdriver.common.actions.pointer_input import PointerInput

# options = AppiumOptions()
# options.load_capabilities({
# 	"platformName": "Android",
# 	"appium:automationName": "UiAutomator2",
# 	"appium:deviceName": "emulator-5554",
# 	"appium:app": "C:\\Users\\shrik\\OneDrive\\Desktop\\Smann_Automation_Testing_STG_Builds\\Tests\\STG_Smann\\Smann_STG_APK\\STG_Smann.apk",
# 	"appium:appPackage": "com.tribetayling.customer.staging",
# 	"appium:appActivity": "com.tribetayling.customer.MainActivity",
# 	"appium:fullReset": True,
# 	"appium:newCommandTimeout": 300,
# 	"appium:ensureWebviewsHavePages": True,
# 	"appium:nativeWebScreenshot": True,
# 	"appium:connectHardwareKeyboard": True
# })

# driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

# el9 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Search “Pizza”")
# el9.click()
# el10 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
# el10.click()
# el10.send_keys("chicken masala")
# el11 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().description(\"Chicken Masala\nProduct\")")
# el11.click()
# el12 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().description(\"Chicken Masala\nProduct\")")
# el12.click()
# el13 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().description(\"Chicken Masala\nProduct\")")
# el13.click()
# el14 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.ImageView\").instance(2)")
# el14.click()
# el15 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().description(\"Chicken Masala\n₹ 172.00\")")
# el15.click()
# el16 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().description(\"Add\").instance(0)")
# el16.click()
# el17 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.Button\").instance(1)")
# el17.click()
# el18 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().description(\"Add\").instance(1)")
# el18.click()
# el19 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="3 items added")
# el19.click()
# el20 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.Button")
# el20.click()
# el21 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.Image\").instance(0)")
# el21.click()
# el22 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.EditText\").instance(0)")
# el22.click()
# el22.send_keys("4100 2800 0000 1007")
# el23 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.EditText\").instance(1)")
# el23.send_keys("12/35")
# el24 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.EditText\").instance(2)")
# el24.send_keys("003")
# el25 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"Continue\")")
# el25.click()
# el26 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"Maybe later\")")
# el26.click()
# el27 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"Success\")")
# el27.click()
# el28 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.ImageView\").instance(11)")
# el28.click()
# el29 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().description(\"King cafe 222\nNew\n#4468\n2 Items\n13 Feb 26 09:37 AM\n₹ 651.84\nONLINE\nSUBMITTED\nDELIVERY\nDetails\")")
# el29.click()
# el30 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.view.View\").instance(7)")
# el30.click()
# el31 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.ImageView\").instance(13)")
# el31.click()
# el32 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Sign out")
# el32.click()
# el33 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Sign Out")
# el33.click()

# driver.quit()


# ==========================================
# Successful Order using Card (Test No)
# Login with test Number and  Fixed OTP (1234)
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
# Helper: Safe Click
# ------------------------------------------
def safe_click(by, value, timeout=5):
    try:
        el = WebDriverWait(driver, timeout).until(EC.element_to_be_clickable((by, value)))
        el.click()
        return True
    except TimeoutException:
        return False

# ------------------------------------------
# Helper: Handle Permissions
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
# Login Flow (Same as Login_logout_TestNum)
# ------------------------------------------
mobile_input = wait.until(EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText")))
mobile_input.click()
mobile_input.clear()
mobile_input.send_keys(PHONE_NUMBER)

continue_btn = wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Continue")))
continue_btn.click()

print("📲 Magic number entered, proceeding with fixed OTP...")

def enter_otp_safely(otp):
    print("✍️ Entering FIXED OTP safely...")
    for attempt in range(1, 4):
        try:
            driver.activate_app(APP_PACKAGE)
            time.sleep(1)

            otp_input = wait.until(EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText")))
            otp_input.click()
            time.sleep(1)
            try:
                otp_input.clear()
            except:
                pass
            time.sleep(1)

            os.system(f'adb -s {DEVICE_UDID} shell input text {otp}')
            print(f"⌨️ Fixed OTP typed via ADB (attempt {attempt})")

            WebDriverWait(driver, 15).until(
                EC.any_of(
                    EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Got it! Thanks")),
                    EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Order Now")),
                    EC.presence_of_element_located(
                        (AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.ImageView")')
                    )
                )
            )
            print("✅ OTP accepted, moved to next screen")
            return True

        except Exception as e:
            print(f"⚠️ Retry OTP entry (attempt {attempt}): {e}")
            time.sleep(2)

    raise Exception("❌ Failed to move past OTP screen")

enter_otp_safely(FIXED_OTP)

handle_permissions()
handle_intro_templates()

print("🏠 Reached Home Page")

# ==================================================
# =============== ORDER FLOW (RECORDED) =============
# ==================================================

# Search
search_btn = wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, 'Search “Pizza”')))
search_btn.click()

search_input = wait.until(EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText")))
search_input.send_keys("chicken masala")

product = wait.until(
    EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("Chicken Masala")'))
)
product.click()
product.click()
product.click()

open_item = wait.until(
    EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.ImageView").instance(2)'))
)
open_item.click()

select_item = wait.until(
    EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().descriptionContains("₹")'))
)
select_item.click()

add_btn = wait.until(
    EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Add").instance(0)'))
)
add_btn.click()

confirm_btn = wait.until(
    EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.Button").instance(1)'))
)
confirm_btn.click()

add_btn2 = wait.until(
    EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().description("Add").instance(1)'))
)
add_btn2.click()

cart_btn = wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "3 items added")))
cart_btn.click()

place_order_btn = wait.until(EC.element_to_be_clickable((AppiumBy.CLASS_NAME, "android.widget.Button")))
place_order_btn.click()

# ------------------------------------------
# Payment - FIXED CARD CLICK
# ------------------------------------------
print("💳 Selecting Card option...")

# Try normal click first
try:
    card_option = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.Image").instance(0)'))
    )
    card_option.click()
except:
    # Fallback: scroll & try again
    driver.find_element(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiScrollable(new UiSelector().scrollable(true)).scrollForward()'
    )
    card_option = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.Image").instance(0)'))
    )
    card_option.click()

# Enter card details
card_number = wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(0)')))
card_number.send_keys("4100280000001007")

expiry = wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(1)')))
expiry.send_keys("12/35")

cvv = wait.until(EC.presence_of_element_located((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.EditText").instance(2)')))
cvv.send_keys("003")

continue_btn = wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Continue")')))
continue_btn.click()

# Post payment
try:
    maybe_later = wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Maybe later")')))
    maybe_later.click()
except TimeoutException:
    pass

success = wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Success")')))
success.click()

print("✅ Order placed successfully")

# ------------------------------------------
# Logout
# ------------------------------------------
menu_icon = wait.until(EC.element_to_be_clickable((AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().className("android.widget.ImageView").instance(13)')))
menu_icon.click()

safe_click(AppiumBy.ACCESSIBILITY_ID, "Sign out", 10)
safe_click(AppiumBy.ACCESSIBILITY_ID, "Sign Out", 10)

print("✅ Logout completed")

# ------------------------------------------
# Cleanup
# ------------------------------------------
time.sleep(2)
driver.quit()
print("✅ Test execution finished")
