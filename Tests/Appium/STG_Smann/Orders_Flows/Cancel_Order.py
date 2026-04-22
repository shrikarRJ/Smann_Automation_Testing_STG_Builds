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
el6 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Order Now")
el6.click()
el7 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Home-1-2-3-4-5-6-7-8-9")
el7.click()
el8 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Add Address")
el8.click()
el9 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.EditText\").instance(0)")
el9.click()
el9.send_keys("railway station")
el10 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.EditText\").instance(1)")
el10.click()
el10.send_keys("khopoli")
driver.execute_script('mobile:pressKey', {"keycode": 4})
el11 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Confirm Address")
el11.click()
el12 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.Button\").instance(0)")
el12.click()
el13 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="FOOD")
el13.click()
el14 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().description(\"King cafe 222\n21 mins\n0.3 km\")")
el14.click()
el15 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Menu")
el15.click()
el16 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().description(\"Add\").instance(0)")
el16.click()
el17 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().description(\"Add\").instance(0)")
el17.click()
el18 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="2 items added")
el18.click()
actions = ActionChains(driver)
actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
actions.w3c_actions.pointer_action.move_to_location(542, 1730)
actions.w3c_actions.pointer_action.pointer_down()
actions.w3c_actions.pointer_action.move_to_location(567, 279)
actions.w3c_actions.pointer_action.release()
actions.perform()

el19 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.Button")
el19.click()
el20 = driver.find_element(by=AppiumBy.CLASS_NAME, value="android.widget.EditText")
el20.click()
el20.send_keys("9021004607")
el21 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.Image\").instance(5)")
el21.click()
el22 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"Axis Axis Facing issues\")")
el22.click()
el23 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().text(\"Success\")")
el23.click()
el24 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.ImageView\").instance(9)")
el24.click()
el25 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().description(\"King cafe 222\nNew\n#4757\n2 Items\n01 Mar 26 02:27 AM\n₹ 386.20\nONLINE\nSUBMITTED\nDELIVERY\nDetails\")")
el25.click()
actions = ActionChains(driver)
actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
actions.w3c_actions.pointer_action.move_to_location(554, 2064)
actions.w3c_actions.pointer_action.pointer_down()
actions.w3c_actions.pointer_action.pause(0.1)
actions.w3c_actions.pointer_action.release()
actions.perform()

el26 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Reject Order")
el26.click()
el27 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.view.View\").instance(7)")
el27.click()
el28 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().description(\"King cafe 222\nNew\n#4757\n2 Items\n01 Mar 26 02:27 AM\n₹ 386.20\nONLINE\nCANCELLED\nDELIVERY\nDetails\")")
el28.click()
el29 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.view.View\").instance(7)")
el29.click()
el30 = driver.find_element(by=AppiumBy.ANDROID_UIAUTOMATOR, value="new UiSelector().className(\"android.widget.ImageView\").instance(12)")
el30.click()
el31 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Sign out")
el31.click()
el32 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value="Sign Out")
el32.click()

driver.quit()
