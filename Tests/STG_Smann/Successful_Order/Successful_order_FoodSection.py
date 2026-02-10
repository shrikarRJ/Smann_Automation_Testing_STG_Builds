# # ==========================================
# # Stable Appium Automation Script
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
#     "appium:deviceName": "ZA222KCFFQ",
#     "appium:app": r"C:\Users\shrik\OneDrive\Desktop\Smann_Automation_Testing_STG_Builds\Tests\STG_Smann\Smann_STG_APK\STG_Smann.apk",
#     "appium:appPackage": "com.tribetayling.customer.staging",
#     "appium:appActivity": "com.tribetayling.customer.MainActivity",

#     # 🔴 CRITICAL FIX
#     "appium:noReset": True,
#     "appium:newCommandTimeout": 300
# })

# ZA222KCFFQ
# ZA222KCFFQ

# # ------------------------------------------
# # Driver Initialization
# # ------------------------------------------
# driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
# wait = WebDriverWait(driver, 30)

# print("✅ App launched")

# # ------------------------------------------
# # Landing Screen → Login
# # ------------------------------------------
# try:
#     landing = wait.until(
#         EC.element_to_be_clickable(
#             (AppiumBy.ANDROID_UIAUTOMATOR,
#              'new UiSelector().descriptionContains("Log in or Sign up")')
#         )
#     )
#     landing.click()
# except TimeoutException:
#     print("ℹ️ Login screen already open")

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
# # OTP
# # ------------------------------------------
# otp_input = wait.until(
#     EC.presence_of_element_located(
#         (AppiumBy.CLASS_NAME, "android.widget.EditText")
#     )
# )
# otp_input.send_keys("1234")

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
#     got_it = wait.until(
#         EC.element_to_be_clickable(
#             (AppiumBy.ACCESSIBILITY_ID, "Got it! Thanks")
#         )
#     )
#     got_it.click()
# except TimeoutException:
#     print("ℹ️ Offer popup not shown")

# # ------------------------------------------
# # FOOD Tab
# # ------------------------------------------
# food_tab = wait.until(
#     EC.element_to_be_clickable(
#         (AppiumBy.ACCESSIBILITY_ID, "FOOD")
#     )
# )
# food_tab.click()

# # ------------------------------------------
# # Restaurant Selection
# # ------------------------------------------
# restaurant = wait.until(
#     EC.presence_of_element_located(
#         (AppiumBy.ANDROID_UIAUTOMATOR,
#          'new UiSelector().descriptionContains("King cafe")')
#     )
# )
# restaurant.click()

# menu_tab = wait.until(
#     EC.element_to_be_clickable(
#         (AppiumBy.ACCESSIBILITY_ID, "Menu")
#     )
# )
# menu_tab.click()

# # ------------------------------------------
# # Add Items
# # ------------------------------------------
# add_item_1 = wait.until(
#     EC.element_to_be_clickable(
#         (AppiumBy.ANDROID_UIAUTOMATOR,
#          'new UiSelector().description("Add").instance(0)')
#     )
# )
# add_item_1.click()

# add_item_2 = wait.until(
#     EC.element_to_be_clickable(
#         (AppiumBy.ANDROID_UIAUTOMATOR,
#          'new UiSelector().description("Add").instance(1)')
#     )
# )
# add_item_2.click()

# confirm_add = wait.until(
#     EC.element_to_be_clickable(
#         (AppiumBy.ANDROID_UIAUTOMATOR,
#          'new UiSelector().className("android.widget.Button").instance(3)')
#     )
# )
# confirm_add.click()

# # ------------------------------------------
# # Cart → Place Order
# # ------------------------------------------
# cart_btn = wait.until(
#     EC.element_to_be_clickable(
#         (AppiumBy.ACCESSIBILITY_ID, "3 items added")
#     )
# )
# cart_btn.click()

# place_order = wait.until(
#     EC.element_to_be_clickable(
#         (AppiumBy.ANDROID_UIAUTOMATOR,
#          'new UiSelector().descriptionContains("Place Order")')
#     )
# )
# place_order.click()

# # ------------------------------------------
# # Payment Flow (Test Card)
# # ------------------------------------------
# card_option = wait.until(
#     EC.element_to_be_clickable(
#         (AppiumBy.ANDROID_UIAUTOMATOR,
#          'new UiSelector().className("android.widget.Image").instance(2)')
#     )
# )
# card_option.click()

# card_number = wait.until(
#     EC.presence_of_element_located(
#         (AppiumBy.ANDROID_UIAUTOMATOR,
#          'new UiSelector().className("android.widget.EditText").instance(0)')
#     )
# )
# card_number.send_keys("4100280000001007")

# expiry = wait.until(
#     EC.presence_of_element_located(
#         (AppiumBy.ANDROID_UIAUTOMATOR,
#          'new UiSelector().className("android.widget.EditText").instance(1)')
#     )
# )
# expiry.send_keys("0535")

# cvv = wait.until(
#     EC.presence_of_element_located(
#         (AppiumBy.ANDROID_UIAUTOMATOR,
#          'new UiSelector().className("android.widget.EditText").instance(2)')
#     )
# )
# cvv.send_keys("136")

# pay_btn = wait.until(
#     EC.element_to_be_clickable(
#         (AppiumBy.ANDROID_UIAUTOMATOR,
#          'new UiSelector().resourceId("bottom-cta")')
#     )
# )
# pay_btn.click()

# # ------------------------------------------
# # Post Payment Screens
# # ------------------------------------------
# try:
#     maybe_later = wait.until(
#         EC.element_to_be_clickable(
#             (AppiumBy.ANDROID_UIAUTOMATOR,
#              'new UiSelector().text("Maybe later")')
#         )
#     )
#     maybe_later.click()
# except TimeoutException:
#     pass

# success = wait.until(
#     EC.presence_of_element_located(
#         (AppiumBy.ANDROID_UIAUTOMATOR,
#          'new UiSelector().textContains("Success")')
#     )
# )
# success.click()

# # ------------------------------------------
# # Order History → Logout
# # ------------------------------------------
# orders_icon = wait.until(
#     EC.presence_of_element_located(
#         (AppiumBy.ANDROID_UIAUTOMATOR,
#          'new UiSelector().className("android.widget.ImageView").instance(10)')
#     )
# )
# orders_icon.click()

# profile_icon = wait.until(
#     EC.presence_of_element_located(
#         (AppiumBy.ANDROID_UIAUTOMATOR,
#          'new UiSelector().className("android.widget.ImageView").instance(13)')
#     )
# )
# profile_icon.click()

# sign_out = wait.until(
#     EC.element_to_be_clickable(
#         (AppiumBy.ACCESSIBILITY_ID, "Sign out")
#     )
# )
# sign_out.click()

# confirm_signout = wait.until(
#     EC.element_to_be_clickable(
#         (AppiumBy.ACCESSIBILITY_ID, "Sign Out")
#     )
# )
# confirm_signout.click()

# print("✅ Logout completed")

# # ------------------------------------------
# # Cleanup
# # ------------------------------------------
# time.sleep(2)
# driver.quit()
# print("✅ Test execution finished")


# ==========================================
# Stable Appium Automation Script
# Login with TEST NUMBER + FIXED OTP (1234)
# Handles Permissions + Intro Screens Safely
# Then Places Food Order
# ==========================================

from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

# ------------------------------------------
# CONFIG
# ------------------------------------------
TEST_PHONE_NUMBER = "9999999999"
TEST_OTP = "1234"

APK_PATH = r"C:\Users\shrik\OneDrive\Desktop\Smann_Automation_Testing_STG_Builds\Tests\STG_Smann\Smann_STG_APK\STG_Smann.apk"
APP_PACKAGE = "com.tribetayling.customer.staging"
APP_ACTIVITY = "com.tribetayling.customer.MainActivity"

# ------------------------------------------
# Desired Capabilities
# ------------------------------------------
options = AppiumOptions()
options.load_capabilities({
    "platformName": "Android",
    "appium:automationName": "UiAutomator2",
    "appium:deviceName": "ZA222KCFFQ",

    "appium:app": APK_PATH,
    "appium:appPackage": APP_PACKAGE,
    "appium:appActivity": APP_ACTIVITY,

    "appium:noReset": True,
    "appium:autoGrantPermissions": False,   # We will handle manually
    "appium:newCommandTimeout": 300
})

# ------------------------------------------
# Driver Initialization
# ------------------------------------------
driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
wait = WebDriverWait(driver, 40)

print("✅ App launched")

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
# Helper: Handle Permissions (Notification / Location)
# ------------------------------------------
def handle_permissions():
    # Notification / Location / etc.
    if safe_click(AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_button", 3):
        print("✅ Permission allowed")

    if safe_click(AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_foreground_only_button", 3):
        print("✅ Foreground permission allowed")

# ------------------------------------------
# Helper: Handle Intro Templates (Got it / Order Now)
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
# Landing Screen → Login
# ------------------------------------------
try:
    landing = wait.until(
        EC.element_to_be_clickable(
            (AppiumBy.ANDROID_UIAUTOMATOR,
             'new UiSelector().descriptionContains("Log in or Sign up")')
        )
    )
    landing.click()
except TimeoutException:
    print("ℹ️ Login screen already open")

# ------------------------------------------
# Mobile Number Entry
# ------------------------------------------
mobile_input = wait.until(
    EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText"))
)
mobile_input.click()
mobile_input.clear()
mobile_input.send_keys(TEST_PHONE_NUMBER)

continue_btn = wait.until(
    EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Continue"))
)
continue_btn.click()

# ------------------------------------------
# OTP Entry (Fixed 1234)
# ------------------------------------------
otp_input = wait.until(
    EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText"))
)
otp_input.click()
otp_input.clear()
otp_input.send_keys(TEST_OTP)

print("✅ Entered fixed OTP: 1234")

# ------------------------------------------
# Handle Permissions if Shown (Notification / Location)
# ------------------------------------------
handle_permissions()

# ------------------------------------------
# Handle Intro Templates (Got it / Order Now)
# ------------------------------------------
handle_intro_templates()

# ------------------------------------------
# FOOD Tab
# ------------------------------------------
food_tab = wait.until(
    EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "FOOD"))
)
food_tab.click()

# ------------------------------------------
# Restaurant Selection
# ------------------------------------------
restaurant = wait.until(
    EC.presence_of_element_located(
        (AppiumBy.ANDROID_UIAUTOMATOR,
         'new UiSelector().descriptionContains("King cafe")')
    )
)
restaurant.click()

menu_tab = wait.until(
    EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Menu"))
)
menu_tab.click()

# ------------------------------------------
# Add Items
# ------------------------------------------
add_item_1 = wait.until(
    EC.element_to_be_clickable(
        (AppiumBy.ANDROID_UIAUTOMATOR,
         'new UiSelector().description("Add").instance(0)')
    )
)
add_item_1.click()

add_item_2 = wait.until(
    EC.element_to_be_clickable(
        (AppiumBy.ANDROID_UIAUTOMATOR,
         'new UiSelector().description("Add").instance(1)')
    )
)
add_item_2.click()

confirm_add = wait.until(
    EC.element_to_be_clickable(
        (AppiumBy.ANDROID_UIAUTOMATOR,
         'new UiSelector().className("android.widget.Button").instance(3)')
    )
)
confirm_add.click()

# ------------------------------------------
# Cart → Place Order
# ------------------------------------------
cart_btn = wait.until(
    EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "3 items added"))
)
cart_btn.click()

place_order = wait.until(
    EC.element_to_be_clickable(
        (AppiumBy.ANDROID_UIAUTOMATOR,
         'new UiSelector().descriptionContains("Place Order")')
    )
)
place_order.click()

# ------------------------------------------
# Payment Flow (Test Card)
# ------------------------------------------
card_option = wait.until(
    EC.element_to_be_clickable(
        (AppiumBy.ANDROID_UIAUTOMATOR,
         'new UiSelector().className("android.widget.Image").instance(2)')
    )
)
card_option.click()

card_number = wait.until(
    EC.presence_of_element_located(
        (AppiumBy.ANDROID_UIAUTOMATOR,
         'new UiSelector().className("android.widget.EditText").instance(0)')
    )
)
card_number.send_keys("4100280000001007")

expiry = wait.until(
    EC.presence_of_element_located(
        (AppiumBy.ANDROID_UIAUTOMATOR,
         'new UiSelector().className("android.widget.EditText").instance(1)')
    )
)
expiry.send_keys("0535")

cvv = wait.until(
    EC.presence_of_element_located(
        (AppiumBy.ANDROID_UIAUTOMATOR,
         'new UiSelector().className("android.widget.EditText").instance(2)')
    )
)
cvv.send_keys("136")

pay_btn = wait.until(
    EC.element_to_be_clickable(
        (AppiumBy.ANDROID_UIAUTOMATOR,
         'new UiSelector().resourceId("bottom-cta")')
    )
)
pay_btn.click()

# ------------------------------------------
# Post Payment Screens
# ------------------------------------------
try:
    maybe_later = wait.until(
        EC.element_to_be_clickable(
            (AppiumBy.ANDROID_UIAUTOMATOR,
             'new UiSelector().text("Maybe later")')
        )
    )
    maybe_later.click()
except TimeoutException:
    pass

success = wait.until(
    EC.presence_of_element_located(
        (AppiumBy.ANDROID_UIAUTOMATOR,
         'new UiSelector().textContains("Success")')
    )
)
success.click()

print("✅ Order placed successfully")

# ------------------------------------------
# Cleanup
# ------------------------------------------
time.sleep(2)
driver.quit()
print("✅ Test execution finished")
