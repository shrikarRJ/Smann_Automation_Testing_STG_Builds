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

# el1 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
# el1.click()
# el1.send_keys("9021004607")
# el2 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Continue")
# el2.click()
# el3 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
# el3.click()
# el3.send_keys("7888")
# el4 = driver.find_element(by=AppiumBy.ID, value="com.android.permissioncontroller:id/permission_allow_foreground_only_button")
# el4.click()
# el5 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.EditText\").instance(0)")
# el5.click()
# el5.send_keys("Shrikar Jagtap")
# driver.execute_script('mobile:pressKey', {"keycode": 4})
# el6 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Next")
# el6.click()
# el7 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.EditText\").instance(0)")
# el7.click()
# el7.send_keys("Flat 312, Floor 3 ")
# el8 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.EditText\").instance(1)")
# el8.click()
# el8.send_keys("Tower C, Sector 5")
# driver.execute_script('mobile:pressKey', {"keycode": 4})
# el9 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Confirm Address")
# el9.click()
# el10 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().description(\"Get 25% OFF on Your First Order\nGet 25% off up to Rs. 25 on a minimum order value of Rs. 199.\nDon't Miss Out - Shop Now & Save BIG !!\")")
# el10.click()
# el11 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Got it! Thanks")
# el11.click()
# el12 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.ImageView\").instance(8)")
# el12.click()
# el13 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Sign out")
# el13.click()
# el14 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Sign Out")
# el14.click()

# driver.quit()


# ================================
# Stable Appium Automation Script
# ================================

from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time

# -------------------------------
# Desired Capabilities
# -------------------------------
options = AppiumOptions()
options.load_capabilities({
    "platformName": "Android",
    "appium:automationName": "UiAutomator2",
    "appium:deviceName": "emulator-5554",
    "appium:app": "C:\\Users\\shrik\\OneDrive\\Desktop\\Smann_TBT\\STG_Smann\\Smann_STG_APK\\STG_Smann.apk",
    "appium:appPackage": "com.tribetayling.customer.staging",
    "appium:appActivity": "com.tribetayling.customer.MainActivity",
    "appium:noReset": True,              # IMPORTANT
    "appium:newCommandTimeout": 300
})

# -------------------------------
# Driver Initialization
# -------------------------------
driver = webdriver.Remote("http://127.0.0.1:4723", options=options)
wait = WebDriverWait(driver, 30)

print("App launched successfully")

# -------------------------------
# Login / Register - Mobile Number
# -------------------------------
mobile_input = wait.until(
    EC.presence_of_element_located(
        (AppiumBy.CLASS_NAME, "android.widget.EditText")
    )
)
mobile_input.click()
mobile_input.send_keys("9021004607")

continue_btn = wait.until(
    EC.element_to_be_clickable(
        (AppiumBy.ACCESSIBILITY_ID, "Continue")
    )
)
continue_btn.click()

# -------------------------------
# OTP Screen
# -------------------------------
otp_input = wait.until(
    EC.presence_of_element_located(
        (AppiumBy.CLASS_NAME, "android.widget.EditText")
    )
)
otp_input.click()
otp_input.send_keys("1234")

# -------------------------------
# Permission Popup (Optional)
# -------------------------------
try:
    permission_btn = wait.until(
        EC.element_to_be_clickable(
            (AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_foreground_only_button")
        )
    )
    permission_btn.click()
    print("Permission granted")
except TimeoutException:
    print("Permission popup not shown")

# -------------------------------
# Name Entry
# -------------------------------
name_input = wait.until(
    EC.presence_of_element_located(
        (AppiumBy.ANDROID_UIAUTOMATOR,
         'new UiSelector().className("android.widget.EditText").instance(0)')
    )
)
name_input.click()
name_input.send_keys("Shrikar Jagtap")

driver.execute_script("mobile:pressKey", {"keycode": 4})

next_btn = wait.until(
    EC.element_to_be_clickable(
        (AppiumBy.ACCESSIBILITY_ID, "Next")
    )
)
next_btn.click()

# -------------------------------
# Address Entry
# -------------------------------
address_line1 = wait.until(
    EC.presence_of_element_located(
        (AppiumBy.ANDROID_UIAUTOMATOR,
         'new UiSelector().className("android.widget.EditText").instance(0)')
    )
)
address_line1.click()
address_line1.send_keys("Flat 312, Floor 3")

address_line2 = wait.until(
    EC.presence_of_element_located(
        (AppiumBy.ANDROID_UIAUTOMATOR,
         'new UiSelector().className("android.widget.EditText").instance(1)')
    )
)
address_line2.click()
address_line2.send_keys("Tower C, Sector 5")

driver.execute_script("mobile:pressKey", {"keycode": 4})

confirm_address = wait.until(
    EC.element_to_be_clickable(
        (AppiumBy.ACCESSIBILITY_ID, "Confirm Address")
    )
)
confirm_address.click()

# -------------------------------
# Offer Popup
# -------------------------------
offer_popup = wait.until(
    EC.presence_of_element_located(
        (AppiumBy.ANDROID_UIAUTOMATOR,
         'new UiSelector().descriptionContains("Get 25% OFF")')
    )
)
offer_popup.click()

got_it_btn = wait.until(
    EC.element_to_be_clickable(
        (AppiumBy.ACCESSIBILITY_ID, "Got it! Thanks")
    )
)
got_it_btn.click()

# -------------------------------
# Logout Flow
# -------------------------------
profile_icon = wait.until(
    EC.presence_of_element_located(
        (AppiumBy.ANDROID_UIAUTOMATOR,
         'new UiSelector().className("android.widget.ImageView").instance(8)')
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

print("Logout completed successfully")

# -------------------------------
# Cleanup
# -------------------------------
time.sleep(2)
driver.quit()
print("Test execution finished")
