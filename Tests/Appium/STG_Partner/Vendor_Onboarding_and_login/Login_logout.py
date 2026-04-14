# This sample code supports Appium Python client >=2.3.0
# pip install Appium-Python-Client
# Then you can paste this into a file and simply run with Python

from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy

# For W3C actions
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput

options = AppiumOptions()
options.load_capabilities({
	"platformName": "Android",
	"appium:automationName": "UiAutomator2",
	"appium:deviceName": "emulator-5554",
	"appium:app": "C:\\Users\\shrik\\OneDrive\\Desktop\\Smann_Automation_Testing_STG_Builds\\Tests\\STG_Partner\\STG_Partner_Apk\\STG_Partner.apk",
	"appium:appPackage": "com.tribetayling.vendor.staging",
	"appium:appActivity": "com.tribetayling.vendor.MainActivity",
	"appium:fullReset": True,
	"appium:newCommandTimeout": 300,
	"appium:ensureWebviewsHavePages": True,
	"appium:nativeWebScreenshot": True,
	"appium:connectHardwareKeyboard": True
})

driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

el1 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.Button")
el1.click()
el2 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.Button")
el2.click()
el3 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Get started")
el3.click()
el4 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
el4.click()
el4.send_keys("9999990109")
driver.execute_script('mobile:pressKey', {"keycode": 4})
el5 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.CheckBox")
el5.click()
el6 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Get OTP")
el6.click()
el7 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
el7.click()
el7.send_keys("1234")
el8 = driver.find_element(by=AppiumBy.ID, value="com.android.permissioncontroller:id/permission_allow_foreground_only_button")
el8.click()
el9 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Skip")
el9.click()
el10 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.view.View\").instance(32)")
el10.click()
actions = ActionChains(driver)
actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
actions.w3c_actions.pointer_action.move_to_location(434, 1663)
actions.w3c_actions.pointer_action.pointer_down()
actions.w3c_actions.pointer_action.move_to_location(484, 363)
actions.w3c_actions.pointer_action.release()
actions.perform()

el11 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Sign out")
el11.click()
el12 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Sign Out")
el12.click()

driver.quit()