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
	"appium:app": "C:\\Users\\shrik\\OneDrive\\Desktop\\Smann_Automation_Testing_STG_Builds\\Tests\\STG_Smann\\Smann_STG_APK\\STG_Smann.apk",
	"appium:appPackage": "com.tribetayling.customer.staging",
	"appium:appActivity": "com.tribetayling.customer.MainActivity",
	"appium:fullReset": True,
	"appium:newCommandTimeout": 300,
	"appium:ensureWebviewsHavePages": True,
	"appium:nativeWebScreenshot": True,
	"appium:connectHardwareKeyboard": True
})

driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

el8 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
el8.click()
el8.send_keys("9999990001")
el9 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Continue")
el9.click()
el10 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
el10.click()
el10.send_keys("1234")
el11 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.ImageView\").instance(11)")
el11.click()
el12 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Delete Profile")
el12.click()
el13 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Delete")
el13.click()

driver.quit()