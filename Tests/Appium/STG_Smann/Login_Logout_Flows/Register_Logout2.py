from appium import webdriver
from appium.options.common.base import AppiumOptions
from appium.webdriver.common.appiumby import AppiumBy

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException
import os
import subprocess
import time

# ------------------------------------------
# CONFIG
# ------------------------------------------
PHONE_NUMBER = "9999990101"
FIXED_OTP = "1234"
CUSTOMER_NAME = "0101 Test Customer"
ADDRESS_LINE_1 = "0101"
ADDRESS_LINE_2 = "Tower Test"
DELIVERY_LOCATION_QUERY = "Khopoli Bus stand"
DELIVERY_LOCATION_RESULT = (
    "Khopoli ST Stand, Khopoli ST Bus Stand, Laxminagar, Khopoli, Maharashtra, India"
)

DEVICE_UDID = "emulator-5554"

APK_PATH = os.environ.get(
    "APK_PATH",
    r"C:\Users\shrik\OneDrive\Desktop\Smann_Automation_Testing_STG_Builds\Tests\Appium\STG_Smann\Smann_STG_APK\STG_Smann.apk",
)

APP_PACKAGE = "com.tribetayling.customer.staging"
APP_ACTIVITY = "com.tribetayling.customer.MainActivity"
APPIUM_SERVER_URL = "http://127.0.0.1:4723"

OTP_ATTEMPT_MAX = 3
OTP_VERIFY_TIMEOUT = 12
POST_OTP_STATE_TIMEOUT = 20
SHORT_WAIT = 3
LOCATION_CONFIRM_TIMEOUT = 15

driver = None
wait = None


# ------------------------------------------
# Helper: ADB
# ------------------------------------------
def run_adb_command(args, check=True):
    command = ["adb", "-s", DEVICE_UDID, *args]
    result = subprocess.run(command, capture_output=True, text=True)

    if check and result.returncode != 0:
        stderr = result.stderr.strip() or result.stdout.strip()
        raise RuntimeError(f"ADB command failed: {' '.join(command)} :: {stderr}")

    return result


def ensure_app_installed():
    result = run_adb_command(["shell", "pm", "list", "packages", APP_PACKAGE])
    if APP_PACKAGE not in result.stdout:
        print("📦 App not found on device. Installing APK...")
        run_adb_command(["install", "-r", APK_PATH])
        print("✅ App installed")
    else:
        print("✅ App already installed on device")


def reset_app_storage():
    print("🧹 Clearing app data before test run...")
    run_adb_command(["shell", "am", "force-stop", APP_PACKAGE], check=False)
    result = run_adb_command(["shell", "pm", "clear", APP_PACKAGE], check=False)

    clear_output = f"{result.stdout}\n{result.stderr}".strip()
    if "Success" not in clear_output:
        raise RuntimeError(f"Failed to clear app data: {clear_output}")

    print("✅ App data cleared")


# ------------------------------------------
# Helper: Element access
# ------------------------------------------
def safe_click(by, value, timeout=5):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        element.click()
        return True
    except TimeoutException:
        return False


def is_present(by, value, timeout=2):
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )
        return True
    except TimeoutException:
        return False


def get_first_present_locator(locator_groups, timeout=POST_OTP_STATE_TIMEOUT):
    end_time = time.time() + timeout

    while time.time() < end_time:
        for label, by, value in locator_groups:
            if is_present(by, value, 1):
                return label, by, value

        if has_home_address_card():
            return (
                "address chooser",
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().descriptionStartsWith("Home")',
            )

        time.sleep(1)

    raise TimeoutException("Timed out waiting for the expected registration state")


def get_edit_text(index, timeout=10):
    return WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located(
            (
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiSelector().className("android.widget.EditText").instance({index})',
            )
        )
    )


def get_visible_edit_texts(timeout=10, min_count=1):
    def _visible_inputs(_driver):
        elements = _driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
        visible = [element for element in elements if element.is_displayed()]
        return visible if len(visible) >= min_count else False

    return WebDriverWait(driver, timeout).until(_visible_inputs)


def has_home_address_card():
    cards = driver.find_elements(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().descriptionStartsWith("Home")',
    )
    return len(cards) > 0


def log_screen_state(label):
    print(f"🔎 Screen state: {label}")
    snapshots = []

    for by, locator in (
        (AppiumBy.XPATH, "//*[@content-desc]"),
        (AppiumBy.XPATH, "//*[@text]"),
    ):
        try:
            for element in driver.find_elements(by, locator)[:8]:
                value = element.get_attribute("contentDescription") or element.text
                if value:
                    snapshots.append(value.strip())
        except Exception:
            continue

    if snapshots:
        print("   Visible elements:", " | ".join(dict.fromkeys(snapshots)))
    else:
        print("   Visible elements: <not captured>")


# ------------------------------------------
# Helper: Permissions / intro
# ------------------------------------------
def handle_permissions():
    if safe_click(AppiumBy.ACCESSIBILITY_ID, "Enable Location", 5):
        safe_click(
            AppiumBy.ID,
            "com.android.permissioncontroller:id/permission_allow_foreground_only_button",
            5,
        )

    if safe_click(AppiumBy.ACCESSIBILITY_ID, "Enable Notification", 5):
        safe_click(
            AppiumBy.ID,
            "com.android.permissioncontroller:id/permission_allow_button",
            5,
        )

    safe_click(AppiumBy.ID, "com.android.permissioncontroller:id/permission_allow_button", 3)
    safe_click(
        AppiumBy.ID,
        "com.android.permissioncontroller:id/permission_allow_foreground_only_button",
        3,
    )


def handle_intro_templates():
    handle_permissions()

    if safe_click(AppiumBy.ACCESSIBILITY_ID, "Got it! Thanks", 5):
        print("✅ Clicked 'Got it! Thanks'")
        return True

    if safe_click(AppiumBy.ACCESSIBILITY_ID, "Order Now", 5):
        print("✅ Clicked 'Order Now'")
        return True

    return False


# ------------------------------------------
# Helper: Login / OTP
# ------------------------------------------
def enter_mobile_number():
    mobile_input = wait.until(
        EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText"))
    )
    mobile_input.click()
    mobile_input.clear()
    mobile_input.send_keys(PHONE_NUMBER)

    continue_button = wait.until(
        EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Continue"))
    )
    continue_button.click()

    print("📲 Registration number entered, proceeding with fixed OTP...")


def find_and_click_verify_button():
    selectors = (
        ("accessibility id", AppiumBy.ACCESSIBILITY_ID, "Verify"),
        ("button text", AppiumBy.ANDROID_UIAUTOMATOR, 'new UiSelector().text("Verify")'),
        (
            "description contains",
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().descriptionContains("Verify")',
        ),
    )

    for label, by, value in selectors:
        if safe_click(by, value, OTP_VERIFY_TIMEOUT):
            print(f"✅ Verify button clicked via {label}")
            return True

    return False


def wait_for_post_otp_state():
    locator_groups = (
        ("delivery location", AppiumBy.ACCESSIBILITY_ID, "Confirm Delivery Location"),
        ("location permission", AppiumBy.ACCESSIBILITY_ID, "Enable Location"),
        ("notification permission", AppiumBy.ACCESSIBILITY_ID, "Enable Notification"),
        ("name step", AppiumBy.ACCESSIBILITY_ID, "Next"),
        ("address form", AppiumBy.ACCESSIBILITY_ID, "Confirm Address"),
        ("address add button", AppiumBy.ACCESSIBILITY_ID, "Add Address"),
        ("intro screen", AppiumBy.ACCESSIBILITY_ID, "Got it! Thanks"),
        ("home screen", AppiumBy.ACCESSIBILITY_ID, "Order Now"),
        ("profile screen", AppiumBy.ACCESSIBILITY_ID, "Profile"),
    )

    label, _, _ = get_first_present_locator(locator_groups)
    print(f"✅ Post-OTP state detected: {label}")
    return label


def enter_otp_safely(otp):
    print("✍️ Entering fixed OTP safely...")

    for attempt in range(1, OTP_ATTEMPT_MAX + 1):
        try:
            driver.activate_app(APP_PACKAGE)
            time.sleep(1)

            otp_input = wait.until(
                EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText"))
            )
            otp_input.click()
            time.sleep(1)

            try:
                otp_input.clear()
            except Exception:
                pass

            time.sleep(1)
            run_adb_command(["shell", "input", "text", otp])
            time.sleep(2)
            print(f"⌨️ Fixed OTP typed via ADB (attempt {attempt})")
            log_screen_state(f"after OTP entry attempt {attempt}")

            if not find_and_click_verify_button():
                print(f"⚠️ Verify button not found after OTP entry (attempt {attempt})")
                log_screen_state("verify button not found")
                time.sleep(SHORT_WAIT)
                continue

            time.sleep(2)
            wait_for_post_otp_state()
            return True

        except Exception as error:
            print(f"⚠️ Error while entering OTP (attempt {attempt}): {error}")
            log_screen_state(f"OTP attempt {attempt} failed")

        time.sleep(SHORT_WAIT)

    raise Exception("❌ Failed to move past OTP screen after multiple attempts")


# ------------------------------------------
# Helper: Registration flow
# ------------------------------------------
def fill_name():
    name_input = get_edit_text(0)
    name_input.click()
    name_input.clear()
    name_input.send_keys(CUSTOMER_NAME)

    driver.execute_script("mobile:pressKey", {"keycode": 4})

    next_button = wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Next")))
    next_button.click()
    print("✅ Name entered successfully")


def select_delivery_location():
    print(f"📍 Searching delivery location: {DELIVERY_LOCATION_QUERY}")

    safe_click(AppiumBy.ACCESSIBILITY_ID, "Enter location manually", 5)

    search_box = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText"))
    )
    search_box.click()
    search_box.clear()
    search_box.send_keys(DELIVERY_LOCATION_QUERY)
    time.sleep(2)

    result_selectors = (
        ("exact accessibility id", AppiumBy.ACCESSIBILITY_ID, DELIVERY_LOCATION_RESULT),
        (
            "description contains",
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().descriptionContains("Khopoli ST Bus Stand")',
        ),
        (
            "text contains",
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().textContains("Khopoli ST Bus Stand")',
        ),
    )

    for label, by, value in result_selectors:
        if safe_click(by, value, 10):
            print(f"✅ Selected delivery location via {label}: {DELIVERY_LOCATION_RESULT}")
            break
    else:
        suggestions = driver.find_elements(AppiumBy.XPATH, "//*[@text or @content-desc]")
        for suggestion in suggestions:
            try:
                description = (
                    suggestion.get_attribute("contentDescription")
                    or suggestion.get_attribute("text")
                    or suggestion.text
                    or ""
                ).strip()
            except StaleElementReferenceException:
                continue

            if "Khopoli ST Bus Stand" not in description:
                continue

            try:
                suggestion.click()
                print(f"✅ Selected delivery location from visible suggestions: {description}")
                break
            except StaleElementReferenceException:
                continue
        else:
            print("⚠️ Delivery location result for Bus stand Khopoli was not found")
            return False

    confirm_button = WebDriverWait(driver, LOCATION_CONFIRM_TIMEOUT).until(
        EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Confirm Location"))
    )
    confirm_button.click()
    print("✅ Confirmed delivery location")

    WebDriverWait(driver, LOCATION_CONFIRM_TIMEOUT).until(
        EC.any_of(
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Confirm Address")),
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Next")),
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Add Address")),
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Profile")),
        )
    )
    return True


def fill_two_line_address(line_1, line_2, label):
    WebDriverWait(driver, LOCATION_CONFIRM_TIMEOUT).until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Confirm Address"))
    )

    visible_inputs = get_visible_edit_texts(timeout=LOCATION_CONFIRM_TIMEOUT, min_count=3)
    address_inputs = visible_inputs[-3:]
    first_input = address_inputs[0]
    second_input = address_inputs[1]

    def type_and_verify(field, value, field_label):
        for attempt in range(1, 4):
            try:
                field.click()
                time.sleep(1)
                field.clear()
                time.sleep(1)
                field.send_keys(value)
                time.sleep(1)

                entered_value = (
                    field.get_attribute("text")
                    or field.get_attribute("contentDescription")
                    or field.text
                    or ""
                ).strip()

                if value in entered_value or entered_value == value:
                    print(f"✅ {field_label} entered: {entered_value}")
                    return

                print(
                    f"⚠️ {field_label} value not confirmed on attempt {attempt}. "
                    f"Read back: {entered_value or '<empty>'}"
                )
            except StaleElementReferenceException:
                refreshed_inputs = get_visible_edit_texts(timeout=5, min_count=3)[-3:]
                field = refreshed_inputs[0] if field_label == "House / Flat Number" else refreshed_inputs[1]
            except Exception as error:
                print(f"⚠️ Error entering {field_label} on attempt {attempt}: {error}")

            time.sleep(1)

        raise TimeoutException(f"Failed to enter value for {field_label}")

    type_and_verify(first_input, line_1, "House / Flat Number")
    type_and_verify(second_input, line_2, "Tower / Building Name")

    driver.execute_script("mobile:pressKey", {"keycode": 4})
    time.sleep(1)

    confirm_address = wait.until(
        EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Confirm Address"))
    )
    confirm_address.click()
    print(f"✅ {label} entered successfully")


def open_add_address_if_needed():
    if safe_click(AppiumBy.ACCESSIBILITY_ID, "Add Address", 3):
        print("✅ Clicked 'Add Address'")
        return True

    if has_home_address_card():
        home_card = driver.find_elements(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().descriptionStartsWith("Home")',
        )[0]
        home_card.click()
        print("✅ Opened address chooser")
        safe_click(AppiumBy.ACCESSIBILITY_ID, "Add Address", 5)
        return True

    return False


def finish_registration():
    delivery_location_done = False
    name_done = False
    address_details_done = False

    for _ in range(10):
        handle_permissions()

        if is_present(AppiumBy.ACCESSIBILITY_ID, "Profile", 3):
            print("✅ Registration flow reached profile/home state")
            return

        if not delivery_location_done and is_present(
            AppiumBy.ACCESSIBILITY_ID, "Confirm Delivery Location", 3
        ):
            if not select_delivery_location():
                log_screen_state("delivery location suggestion missing")
                raise Exception("❌ Delivery location suggestions were not available")
            delivery_location_done = True
            time.sleep(2)
            continue

        if delivery_location_done and not is_present(
            AppiumBy.ACCESSIBILITY_ID, "Confirm Address", 1
        ) and is_present(
            AppiumBy.ACCESSIBILITY_ID, "Confirm Delivery Location", 2
        ):
            print("⏳ Waiting for delivery location screen to transition after confirmation...")
            time.sleep(2)
            continue

        if not address_details_done and is_present(
            AppiumBy.ACCESSIBILITY_ID, "Confirm Address", 3
        ):
            print("📝 Address detail form detected")
            fill_two_line_address(
                ADDRESS_LINE_1,
                ADDRESS_LINE_2,
                "address details",
            )
            address_details_done = True
            time.sleep(2)
            continue

        if not address_details_done and open_add_address_if_needed():
            time.sleep(2)
            continue

        if not name_done and is_present(AppiumBy.ACCESSIBILITY_ID, "Next", 3):
            fill_name()
            name_done = True
            time.sleep(2)
            continue

        if handle_intro_templates():
            time.sleep(2)
            continue

        if is_present(AppiumBy.ACCESSIBILITY_ID, "Profile", 3):
            print("✅ Registration flow reached profile/home state")
            return

        log_screen_state("unexpected registration state")
        time.sleep(2)

    raise Exception("❌ Registration flow did not reach the home/profile screen")


# ------------------------------------------
# Helper: Profile / logout
# ------------------------------------------
def open_profile():
    try:
        profile_icon = wait.until(
            EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Profile"))
        )
        profile_icon.click()
    except TimeoutException:
        fallback_icon = wait.until(
            EC.element_to_be_clickable(
                (
                    AppiumBy.ANDROID_UIAUTOMATOR,
                    'new UiSelector().className("android.widget.ImageView").instance(8)',
                )
            )
        )
        fallback_icon.click()


def logout_user():
    safe_click(AppiumBy.ACCESSIBILITY_ID, "Sign out", 10)
    safe_click(AppiumBy.ACCESSIBILITY_ID, "Sign Out", 10)
    print("✅ Logout completed successfully")


def wait_for_login_entry_state():
    WebDriverWait(driver, 20).until(
        EC.any_of(
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Continue")),
            EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText")),
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "LogIn")),
        )
    )
    print("✅ Login entry state detected")


def login_existing_user():
    print("🔐 Starting login flow for the registered user...")
    wait_for_login_entry_state()
    handle_permissions()
    enter_mobile_number()
    enter_otp_safely(FIXED_OTP)
    handle_permissions()
    handle_intro_templates()
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Profile"))
    )
    print("✅ User logged back in successfully")


def delete_profile():
    print("🗑️ Starting delete profile flow...")
    open_profile()

    delete_profile_button = wait.until(
        EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Delete Profile"))
    )
    delete_profile_button.click()
    print("✅ Clicked 'Delete Profile'")

    delete_confirmed = False
    for label in ("Delete", "DELETE", "Confirm"):
        if safe_click(AppiumBy.ACCESSIBILITY_ID, label, 5):
            print(f"✅ Confirmed profile deletion via '{label}'")
            delete_confirmed = True
            break

    if not delete_confirmed:
        raise TimeoutException("Delete confirmation button was not available")

    WebDriverWait(driver, 20).until(
        EC.any_of(
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Continue")),
            EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText")),
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "LogIn")),
        )
    )
    print("✅ Profile deleted successfully and user returned to logged-out state")


# ------------------------------------------
# Driver setup
# ------------------------------------------
def create_driver():
    options = AppiumOptions()
    options.load_capabilities(
        {
            "platformName": "Android",
            "appium:automationName": "UiAutomator2",
            "appium:deviceName": "Android",
            "appium:udid": DEVICE_UDID,
            "appium:appPackage": APP_PACKAGE,
            "appium:appActivity": APP_ACTIVITY,
            "appium:noReset": True,
            "appium:autoGrantPermissions": True,
            "appium:newCommandTimeout": 300,
        }
    )
    return webdriver.Remote(APPIUM_SERVER_URL, options=options)


def main():
    global driver, wait

    ensure_app_installed()
    reset_app_storage()

    driver = create_driver()
    wait = WebDriverWait(driver, 40)
    print("✅ App launched successfully")

    handle_permissions()
    enter_mobile_number()
    enter_otp_safely(FIXED_OTP)
    finish_registration()
    open_profile()
    logout_user()
    login_existing_user()
    delete_profile()


if __name__ == "__main__":
    try:
        main()
    finally:
        if driver is not None:
            time.sleep(2)
            driver.quit()
        print("✅ Test execution finished")
