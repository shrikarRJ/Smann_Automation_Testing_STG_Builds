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

el2 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
el2.click()
el3 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
el3.click()
el3.send_keys("9999999999")
el4 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Continue")
el4.click()
el5 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
el5.click()
el5.click()
el5.send_keys("1234")
el6 = driver.find_element(by=AppiumBy.ID, value="com.android.permissioncontroller:id/permission_allow_foreground_only_button")
el6.click()
el7 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="FOOD")
el7.click()
el8 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().description(\"King cafe 222\n21 mins\n0.4 km\")")
el8.click()
el9 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Menu")
el9.click()
el10 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().description(\"Add\").instance(0)")
el10.click()
el11 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().description(\"Add\").instance(0)")
el11.click()
el12 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="2 items added")
el12.click()
el13 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().description(\"₹386.20\nTotal\nPlace Order\")")
el13.click()
el14 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
el14.click()
el15 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"By proceeding, I agree to Razorpay’s \")")
el15.click()
el16 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
el16.click()
el16.send_keys("9021004607")
driver.execute_script('mobile:pressKey', {"keycode": 187})
driver.execute_script('mobile:pressKey', {"keycode": 187})
driver.execute_script('mobile:pressKey', {"keycode": 3})
driver.execute_script('mobile:pressKey', {"keycode": 187})
driver.execute_script('mobile:pressKey', {"keycode": 187})
driver.execute_script('mobile:pressKey', {"keycode": 187})
driver.execute_script('mobile:pressKey', {"keycode": 3})
driver.execute_script('mobile:pressKey', {"keycode": 187})
driver.execute_script('mobile:pressKey', {"keycode": 187})
el17 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.Image\").instance(6)")
el17.click()
el18 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"Axis Axis\")")
el18.click()
el19 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"Success\")")
el19.click()
el20 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.ImageView\").instance(8)")
el20.click()
el21 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.ImageView\").instance(12)")
el21.click()

driver.quit()