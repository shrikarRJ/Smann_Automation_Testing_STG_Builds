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

el1 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
el1.click()
el2 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
el2.click()
el2.send_keys("9999999999")
el3 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Continue")
el3.click()
el4 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
el4.click()
el4.send_keys("1234")
el5 = driver.find_element(by=AppiumBy.ID, value="com.android.permissioncontroller:id/permission_allow_foreground_only_button")
el5.click()
el6 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="FOOD")
el6.click()
el7 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().description(\"King cafe 222\n21 mins\n0.4 km\")")
el7.click()
el8 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Menu")
el8.click()
el9 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().description(\"Add\").instance(0)")
el9.click()
el10 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().description(\"Add\").instance(0)")
el10.click()
el11 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="2 items added")
el11.click()
el12 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().description(\"₹386.20\nTotal\nPlace Order\")")
el12.click()
el13 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
el13.click()
el13.send_keys("9021004607")
el14 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.Image\").instance(6)")
el14.click()
el15 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"BOB BOB\")")
el15.click()

# WAIT HERE FOR 10 MIN

el16 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"Success\")")
el16.click()
el17 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.ImageView\").instance(8)")
el17.click()
el18 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().description(\"King cafe 222\nNew\n#4760\n2 Items\n01 Mar 26 03:36 AM\n₹ 386.20\nONLINE\nCOMPLETED\nDELIVERY\nDetails\")")
el18.click()
el19 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.view.View\").instance(7)")
el19.click()
el20 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.ImageView\").instance(12)")
el20.click()
el21 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Sign out")
el21.click()
el22 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Sign Out")
el22.click()

driver.quit()