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
	"appium:app": "C:\\Users\\shrik\\OneDrive\\Desktop\\Smann_TBT\\STG_Smann\\Smann_STG_APK\\STG_Smann.apk",
	"appium:appPackage": "com.tribetayling.customer.staging",
	"appium:appActivity": "com.tribetayling.customer.MainActivity",
	"appium:fullReset": True,
	"appium:newCommandTimeout": 300,
	"appium:ensureWebviewsHavePages": True,
	"appium:nativeWebScreenshot": True,
	"appium:connectHardwareKeyboard": True
})

driver = webdriver.Remote("http://127.0.0.1:4723", options=options)

el98 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().description(\"India’s #1 Food Delivery \nand Dining App\nLog in or Sign up\n+91 \")")
el98.click()
el99 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
el99.click()
el99.send_keys("9999999999")
el100 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Continue")
el100.click()
el101 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
el101.click()
el101.send_keys("1234")
el102 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Got it! Thanks")
el102.click()
el103 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="FOOD")
el103.click()
el104 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().description(\"King cafe 222\n20 mins\n0.0 km\")")
el104.click()
el105 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Menu")
el105.click()
el106 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().description(\"Add\").instance(0)")
el106.click()
el107 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().description(\"Add\").instance(1)")
el107.click()
el108 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.Button\").instance(3)")
el108.click()
el109 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="3 items added")
el109.click()
el110 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().description(\"₹857.66\nTotal\nPlace Order\")")
el110.click()
el111 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.Image\").instance(2)")
el111.click()
el112 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.EditText\").instance(0)")

el13 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.Image\").instance(2)")
el13.click()



el112.click()
el112.send_keys("4100 2800 0000 1007")
el113 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.EditText\").instance(1)")
el113.click()
el113.send_keys("0535")
el114 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.EditText\").instance(2)")
el114.send_keys("136")
el115 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().resourceId(\"bottom-cta\")")
el115.click()
el116 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"Maybe later\")")
el116.click()

el117 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"Success\")")
el117.click()
el118 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.ImageView\").instance(10)")
el118.click()
el119 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.ImageView\").instance(13)")
el119.click()
el120 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Sign out")
el120.click()
el121 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Sign Out")
el121.click()

driver.quit()