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

e1 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
e1.click()
e1.send_keys("9999999999")
e2 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Continue")
e2.click()
e3 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
e3.click()
e3.send_keys("1234")
e4 = driver.find_element(by=AppiumBy.ID, value="com.android.permissioncontroller:id/permission_allow_foreground_only_button")
e4.click()
e5 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Order Now")
e5.click()


el5 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="FOOD")
el5.click()
el6 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().description(\"King cafe 222\n20 mins\n0.0 km\")")
el6.click()
el7 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Menu")
el7.click()
el8 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().description(\"Add\").instance(0)")
el8.click()
el9 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().description(\"Add\").instance(0)")
el9.click()
el10 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="2 items added")
el10.click()
actions = ActionChains(driver)
actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
actions.w3c_actions.pointer_action.move_to_location(475, 1593)
actions.w3c_actions.pointer_action.pointer_down()
actions.w3c_actions.pointer_action.move_to_location(559, 384)
actions.w3c_actions.pointer_action.release()
actions.perform()
el11 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().description(\"Delivery at Home-1-2-3-4-5-6-7-8-9-10-11\nBus stand, khopoli, Khopoli ST Bus Stand, Laxminagar, Khopoli, Maharashtra 410203, India\")")
el11.click()
el12 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().description(\"Select Address\nAdd New\")")
el12.click()
el13 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().description(\"Delivery at Home-1-2-3-4-5\n9999,99,2ED, Yashwant Nagar, Khopoli, Maharashtra 410203, India\")")
el13.click()
el14 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.EditText\").instance(0)")
el14.click()
el14.send_keys("change address")
el15 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.EditText\").instance(1)")
el15.click()
el15.send_keys("railway khopoli")
driver.execute_script('mobile:pressKey', {"keycode": 4})
el16 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Confirm Address")
el16.click()
el17 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.Button")
el17.click()
el18 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
el18.click()
el18.send_keys("9021004607")
el19 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.Image\").instance(6)")
el19.click()
el20 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"Axis Axis\")")
el20.click()
el21 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"Success\")")
el21.click()
el22 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.ImageView\").instance(8)")
el22.click()
el23 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().description(\"King cafe 222\nNew\n#4760\n2 Items\n01 Mar 26 03:36 AM\n₹ 386.20\nONLINE\nSUBMITTED\nDELIVERY\nDetails\")")
el23.click()
el24 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.view.View\").instance(7)")
el24.click()
el25 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.ImageView\").instance(12)")
el25.click()
el26 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Sign out")
el26.click()
el27 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Sign Out")
el27.click()



