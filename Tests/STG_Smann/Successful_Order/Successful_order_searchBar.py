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
# 	"appium:app": "C:\\Users\\shrik\\OneDrive\\Desktop\\Smann_TBT\\STG_Smann\\Smann_STG_APK\\STG_Smann.apk",
# 	"appium:appPackage": "com.tribetayling.customer.staging",
# 	"appium:appActivity": "com.tribetayling.customer.MainActivity",
# 	"appium:fullReset": True,
# 	"appium:newCommandTimeout": 300,
# 	"appium:ensureWebviewsHavePages": True,
# 	"appium:nativeWebScreenshot": True,
# 	"appium:connectHardwareKeyboard": True
# })

# driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

# el175 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
# el175.click()
# el175.send_keys("9999999999")
# el176 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Continue")
# el176.click()
# el177 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
# el177.click()
# el177.send_keys("1234")
# el178 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Search “Pizza”")
# el178.click()
# el179 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
# el179.click()
# el179.send_keys("samosa")
# el180 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.ImageView\").instance(1)")
# el180.click()
# el181 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().description(\"CHOLE SAMOSA FUSION\n₹ 75.00\")")
# el181.click()
# el182 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().description(\"Add\").instance(0)")
# el182.click()
# el183 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().description(\"Add\").instance(0)")
# el183.click()
# el184 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.Button\").instance(3)")
# el184.click()
# el185 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="3 items added")
# el185.click()
# el186 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().description(\"₹180.00\nTotal\nPlace Order\")")
# el186.click()
# el187 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.ImageView\").instance(10)")
# el187.click()
# el188 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().description(\"test\nNew\n#4122\n2 Items\n02 Feb 26 05:15 PM\n₹ 180.00\nCASH\nSUBMITTED\nDELIVERY\nDetails\")")
# el188.click()
# el189 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.view.View\").instance(7)")
# el189.click()
# el190 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.ImageView\").instance(13)")
# el190.click()
# el191 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Sign out")
# el191.click()
# el192 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Sign Out")
# el192.click()

# driver.quit()


# ==========================================
# Stable Appium Automation Script
# ==========================================

from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

# ------------------------------------------
# Desired Capabilities (FIXED)
# ------------------------------------------
options = AppiumOptions()
options.load_capabilities({
    "platformName": "Android",
    "appium:automationName": "UiAutomator2",
    "appium:deviceName": "emulator-5554",
    "appium:app": "C:\\Users\\shrik\\OneDrive\\Desktop\\Smann_TBT\\STG_Smann\\Smann_STG_APK\\STG_Smann.apk",
    "appium:appPackage": "com.tribetayling.customer.staging",
    "appium:appActivity": "com.tribetayling.customer.MainActivity",

    # 🔴 CRITICAL FIX
    "appium:noReset": True,      # Prevent reinstall every run
    "appium:newCommandTimeout": 300
})

# ------------------------------------------
# Driver Initialization
# ------------------------------------------
driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
wait = WebDriverWait(driver, 30)

print("✅ App launched")

# ------------------------------------------
# Login - Mobile Number
# ------------------------------------------
mobile_input = wait.until(
    EC.presence_of_element_located(
        (AppiumBy.CLASS_NAME, "android.widget.EditText")
    )
)
mobile_input.click()
mobile_input.send_keys("9999999999")

continue_btn = wait.until(
    EC.element_to_be_clickable(
        (AppiumBy.ACCESSIBILITY_ID, "Continue")
    )
)
continue_btn.click()

# ------------------------------------------
# OTP Entry
# ------------------------------------------
otp_input = wait.until(
    EC.presence_of_element_located(
        (AppiumBy.CLASS_NAME, "android.widget.EditText")
    )
)
otp_input.click()
otp_input.send_keys("1234")

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
# Search Entry Point
# ------------------------------------------
search_entry = wait.until(
    EC.element_to_be_clickable(
        (AppiumBy.ACCESSIBILITY_ID, 'Search “Pizza”')
    )
)
search_entry.click()

search_box = wait.until(
    EC.presence_of_element_located(
        (AppiumBy.CLASS_NAME, "android.widget.EditText")
    )
)
search_box.send_keys("samosa")

search_result_icon = wait.until(
    EC.presence_of_element_located(
        (AppiumBy.ANDROID_UIAUTOMATOR,
         'new UiSelector().className(\"android.widget.ImageView\").instance(1)')
    )
)
search_result_icon.click()

# ------------------------------------------
# Select Item & Add to Cart
# ------------------------------------------
item_card = wait.until(
    EC.presence_of_element_located(
        (AppiumBy.ANDROID_UIAUTOMATOR,
         'new UiSelector().descriptionContains(\"CHOLE SAMOSA FUSION\n₹ 75.00\")')
    )
)
item_card.click()

add_btn_1 = wait.until(
    EC.element_to_be_clickable(
        (AppiumBy.ANDROID_UIAUTOMATOR,
         'new UiSelector().description(\"Add\").instance(0)')
    )
)
add_btn_1.click()

add_btn_2 = wait.until(
    EC.element_to_be_clickable(
        (AppiumBy.ANDROID_UIAUTOMATOR,
         'new UiSelector().description(\"Add\").instance(0)')
    )
)
add_btn_2.click()

confirm_add_btn = wait.until(
    EC.element_to_be_clickable(
        (AppiumBy.ANDROID_UIAUTOMATOR,
         'new UiSelector().className("android.widget.Button").instance(3)')
    )
)
confirm_add_btn.click()

# ------------------------------------------
# Cart & Place Order
# ------------------------------------------
cart_btn = wait.until(
    EC.element_to_be_clickable(
        (AppiumBy.ACCESSIBILITY_ID, "3 items added")
    )
)
cart_btn.click()

place_order_btn = wait.until(
    EC.element_to_be_clickable(
        (AppiumBy.ANDROID_UIAUTOMATOR,
         'new UiSelector().descriptionContains("Place Order")')
    )
)
place_order_btn.click()

# ------------------------------------------
# Order History
# ------------------------------------------
order_history_icon = wait.until(
    EC.presence_of_element_located(
        (AppiumBy.ANDROID_UIAUTOMATOR,
         'new UiSelector().className("android.widget.ImageView").instance(10)')
    )
)
order_history_icon.click()

order_card = wait.until(
    EC.presence_of_element_located(
        (AppiumBy.ANDROID_UIAUTOMATOR,
         'new UiSelector().descriptionContains("SUBMITTED")')
    )
)
order_card.click()

back_btn = wait.until(
    EC.presence_of_element_located(
        (AppiumBy.ANDROID_UIAUTOMATOR,
         'new UiSelector().className("android.view.View").instance(7)')
    )
)
back_btn.click()

# ------------------------------------------
# Logout Flow
# ------------------------------------------
profile_icon = wait.until(
    EC.presence_of_element_located(
        (AppiumBy.ANDROID_UIAUTOMATOR,
         'new UiSelector().className("android.widget.ImageView").instance(13)')
    )
)
profile_icon.click()

sign_out_btn = wait.until(
    EC.element_to_be_clickable(
        (AppiumBy.ACCESSIBILITY_ID, "Sign out")
    )
)
sign_out_btn.click()

confirm_signout = wait.until(
    EC.element_to_be_clickable(
        (AppiumBy.ACCESSIBILITY_ID, "Sign Out")
    )
)
confirm_signout.click()

print("✅ Logout completed")

# ------------------------------------------
# Cleanup
# ------------------------------------------
time.sleep(2)
driver.quit()
print("✅ Test execution finished")
