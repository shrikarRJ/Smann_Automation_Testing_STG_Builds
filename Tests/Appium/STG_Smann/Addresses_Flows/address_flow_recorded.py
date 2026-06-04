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
	"appium:app": "C:\\Users\\shrik\\OneDrive\\Desktop\\Smann_Automation_Testing_STG_Builds\\Tests\\Appium\\STG_Smann\\Smann_STG_APK\\STG_Smann.apk",
	"appium:appPackage": "com.tribetayling.customer.staging",
	"appium:appActivity": "com.tribetayling.customer.MainActivity",
	"appium:fullReset": True,
	"appium:newCommandTimeout": 300,
	"appium:ensureWebviewsHavePages": True,
	"appium:nativeWebScreenshot": True,
	"appium:connectHardwareKeyboard": True
})

driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

el36 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
el36.click()
el36.send_keys("9999990102")
el37 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Continue")
el37.click()
el38 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
el38.click()
el38.send_keys("1234")
el39 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Home-1-2-3-4-5-6-7-8-9-10")
el39.click()
el40 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Add Address")
el40.click()
el41 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.EditText\").instance(0)")
el41.click()
el41.send_keys("Bus stand")
el42 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.EditText\").instance(1)")
el42.click()
el42.send_keys("khopoli")
driver.execute_script('mobile:pressKey', {"keycode": 4})
el43 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Confirm Address")
el43.click()
el44 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.Button\").instance(0)")
el44.click()

driver.quit()
