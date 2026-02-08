# # ==========================================
# # Login_Logout
# # ==========================================

# from appium import webdriver
# from appium.options.common.base import AppiumOptions
# from appium.webdriver.common.appiumby import AppiumBy

# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
# import time

# # ------------------------------------------
# # Desired Capabilities (FIXED)
# # ------------------------------------------
# options = AppiumOptions()
# options.load_capabilities({
#     "platformName": "Android",
#     "appium:automationName": "UiAutomator2",
#     "appium:deviceName": "emulator-5554",
#     "appium:app": "C:\\Users\\shrik\\OneDrive\\Desktop\\Smann_TBT\\STG_Smann\\Smann_STG_APK\\STG_Smann.apk",
#     "appium:appPackage": "com.tribetayling.customer.staging",
#     "appium:appActivity": "com.tribetayling.customer.MainActivity",

#     # IMPORTANT FIXES
#     "appium:noReset": True,              # Do NOT reinstall app every run
#     "appium:newCommandTimeout": 300
# })

# # ------------------------------------------
# # Driver Initialization
# # ------------------------------------------
# driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
# wait = WebDriverWait(driver, 30)

# print("✅ App launched successfully")

# # ------------------------------------------
# # Mobile Number Entry
# # ------------------------------------------
# mobile_input = wait.until(
#     EC.presence_of_element_located(
#         (AppiumBy.CLASS_NAME, "android.widget.EditText")
#     )
# )
# mobile_input.click()
# mobile_input.send_keys("9999999999")

# continue_btn = wait.until(
#     EC.element_to_be_clickable(
#         (AppiumBy.ACCESSIBILITY_ID, "Continue")
#     )
# )
# continue_btn.click()

# # ------------------------------------------
# # OTP Entry
# # ------------------------------------------
# otp_input = wait.until(
#     EC.presence_of_element_located(
#         (AppiumBy.CLASS_NAME, "android.widget.EditText")
#     )
# )
# otp_input.click()
# otp_input.send_keys("1234")

# # ------------------------------------------
# # Permission Popup (Only First Time)
# # ------------------------------------------
# try:
#     permission_btn = wait.until(
#         EC.element_to_be_clickable(
#             (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_foreground_only_button")
#         )
#     )
#     permission_btn.click()
#     print("✅ Permission granted")
# except TimeoutException:
#     print("ℹ️ Permission popup not shown")

# # ------------------------------------------
# # Offer Popup
# # ------------------------------------------
# try:
#     got_it_btn = wait.until(
#         EC.element_to_be_clickable(
#             (AppiumBy.ACCESSIBILITY_ID, "Got it! Thanks")
#         )
#     )
#     got_it_btn.click()
# except TimeoutException:
#     print("ℹ️ Offer popup not shown")

# # ------------------------------------------
# # Profile / Menu Icon
# # ------------------------------------------
# profile_icon = wait.until(
#     EC.element_to_be_clickable(
#         (AppiumBy.ANDROID_UIAUTOMATOR,
#          'new UiSelector().className(\"android.widget.ImageView\").instance(13)')
#     )
# )
# profile_icon.click()

# # ------------------------------------------
# # Logout Flow
# # ------------------------------------------
# sign_out_btn = wait.until(
#     EC.element_to_be_clickable(
#         (AppiumBy.ACCESSIBILITY_ID, "Sign out")
#     )
# )
# sign_out_btn.click()

# confirm_signout = wait.until(
#     EC.presence_of_element_located(
#         (AppiumBy.ANDROID_UIAUTOMATOR,
#          'new UiSelector().className("android.view.View").instance(7)')
#     )
# )
# confirm_signout.click()

# print("✅ Logout completed successfully")

# # ------------------------------------------
# # Cleanup
# # ------------------------------------------
# time.sleep(2)
# driver.quit()
# print("✅ Test execution finished")






# ==========================================
# Login_Logout with API OTP
# ==========================================

from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import requests

# ------------------------------------------
# CONFIG
# ------------------------------------------
PHONE_NUMBER = "9021004607"

# 🔴 REPLACE THIS WITH YOUR REAL OTP API ENDPOINT
# Example: https://stg-api.yourapp.com/test/otp?phone=9021004607
OTP_API_URL = "https://stg-api.yourapp.com/test/otp?phone="

# ------------------------------------------
# Helper: Fetch OTP from Backend API
# ------------------------------------------
def fetch_otp_from_api(phone):
    print("📡 Fetching OTP from backend API...")
    url = OTP_API_URL + phone

    # You may need headers / auth token depending on your API
    # headers = {"Authorization": "Bearer YOUR_TOKEN"}
    # response = requests.get(url, headers=headers)

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()

    # 🔴 Adjust this based on your API response structure
    # Example response: { "otp": "483921" }
    otp = data.get("otp")

    if not otp:
        raise Exception("❌ OTP not found in API response")

    print(f"✅ OTP fetched: {otp}")
    return otp

# ------------------------------------------
# Desired Capabilities
# ------------------------------------------

options = AppiumOptions()
options.load_capabilities({
    "platformName": "Android",
    "appium:automationName": "UiAutomator2",
    "appium:deviceName": "emulator-5554",
    "appium:app": "C:\\Users\\shrik\\OneDrive\\Desktop\\Smann_Automation_Testing_STG_Builds\\Tests\\STG_Smann\\Smann_STG_APK\\STG_Smann.apk",
    "appium:appPackage": "com.tribetayling.customer.staging",
    "appium:appActivity": "com.tribetayling.customer.MainActivity",

    # IMPORTANT FIXES
    "appium:noReset": True,
    "appium:newCommandTimeout": 300
})

# ZA222KCFFQ
# emulator-5554

# ------------------------------------------
# Driver Initialization
# ------------------------------------------
driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
wait = WebDriverWait(driver, 30)

print("✅ App launched successfully")

# ------------------------------------------
# Mobile Number Entry
# ------------------------------------------
mobile_input = wait.until(
    EC.presence_of_element_located(
        (AppiumBy.CLASS_NAME, "android.widget.EditText")
    )
)
mobile_input.click()
mobile_input.send_keys(PHONE_NUMBER)

continue_btn = wait.until(
    EC.element_to_be_clickable(
        (AppiumBy.ACCESSIBILITY_ID, "Continue")
    )
)
continue_btn.click()

# ------------------------------------------
# Fetch OTP from API
# ------------------------------------------
# Small wait to ensure OTP is generated on backend
time.sleep(3)

otp_value = fetch_otp_from_api(PHONE_NUMBER)

# ------------------------------------------
# OTP Entry
# ------------------------------------------
otp_input = wait.until(
    EC.presence_of_element_located(
        (AppiumBy.CLASS_NAME, "android.widget.EditText")
    )
)
otp_input.click()
otp_input.send_keys(otp_value)

# ------------------------------------------
# Permission Popup (Only First Time)
# ------------------------------------------
try:
    permission_btn = wait.until(
        EC.element_to_be_clickable(
            (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_foreground_only_button")
        )
    )
    permission_btn.click()
    print("✅ Permission granted")
except TimeoutException:
    print("ℹ️ Permission popup not shown")

# ------------------------------------------
# Offer Popup
# ------------------------------------------
try:
    got_it_btn = wait.until(
        EC.element_to_be_clickable(
            (AppiumBy.ACCESSIBILITY_ID, "Got it! Thanks")
        )
    )
    got_it_btn.click()
except TimeoutException:
    print("ℹ️ Offer popup not shown")

# ------------------------------------------
# Profile / Menu Icon
# ------------------------------------------
profile_icon = wait.until(
    EC.element_to_be_clickable(
        (AppiumBy.ANDROID_UIAUTOMATOR,
         'new UiSelector().className("android.widget.ImageView").instance(13)')
    )
)
profile_icon.click()

# ------------------------------------------
# Logout Flow
# ------------------------------------------
sign_out_btn = wait.until(
    EC.element_to_be_clickable(
        (AppiumBy.ACCESSIBILITY_ID, "Sign out")
    )
)
sign_out_btn.click()

confirm_signout = wait.until(
    EC.presence_of_element_located(
        (AppiumBy.ANDROID_UIAUTOMATOR,
         'new UiSelector().className("android.view.View").instance(7)')
    )
)
confirm_signout.click()

print("✅ Logout completed successfully")

# ------------------------------------------
# Cleanup
# ------------------------------------------
time.sleep(2)
driver.quit()
print("✅ Test execution finished")
