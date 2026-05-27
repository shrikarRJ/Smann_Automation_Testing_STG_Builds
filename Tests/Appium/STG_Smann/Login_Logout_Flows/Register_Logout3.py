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

DEVICE_UDID = "ZA222KCFFQ"

# ZA222KCFFQ
# emulator-5554

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
PHONE_ENTRY_ATTEMPT_MAX = 3
PHONE_TO_OTP_TIMEOUT = 8
WAIT_POLL_INTERVAL = 0.2
FAST_CHECK_TIMEOUT = 0.8
STATE_CHECK_TIMEOUT = 1.5
PERMISSION_WAIT_TIMEOUT = 1.2
UI_SETTLE_DELAY = 0.2
FIELD_RETRY_DELAY = 0.3
FLOW_SETTLE_DELAY = 0.4
INTRO_WAIT_TIMEOUT = 1.0
PROFILE_WAIT_TIMEOUT = 6
SEARCH_RESULT_TIMEOUT = 8

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
def build_wait(timeout):
    return WebDriverWait(
        driver,
        timeout,
        poll_frequency=WAIT_POLL_INTERVAL,
        ignored_exceptions=(StaleElementReferenceException,),
    )


def get_first_element(by, value, displayed_only=False):
    try:
        elements = driver.find_elements(by, value)
    except Exception:
        return None

    for element in elements:
        try:
            if not displayed_only or element.is_displayed():
                return element
        except StaleElementReferenceException:
            continue

    return None


def safe_click(by, value, timeout=5):
    try:
        element = build_wait(timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        element.click()
        return True
    except TimeoutException:
        return False


def click_if_present(by, value, timeout=FAST_CHECK_TIMEOUT):
    element = get_first_element(by, value, displayed_only=True)
    if element is not None:
        try:
            element.click()
            return True
        except Exception:
            pass

    return safe_click(by, value, timeout)


def is_present(by, value, timeout=FAST_CHECK_TIMEOUT):
    end_time = time.perf_counter() + max(timeout, 0)

    while True:
        if get_first_element(by, value) is not None:
            return True

        if timeout <= 0 or time.perf_counter() >= end_time:
            return False

        time.sleep(WAIT_POLL_INTERVAL)


def get_first_present_locator(locator_groups, timeout=POST_OTP_STATE_TIMEOUT):
    end_time = time.perf_counter() + timeout

    while time.perf_counter() < end_time:
        for label, by, value in locator_groups:
            if is_present(by, value, 0):
                return label, by, value

        if has_home_address_card():
            return (
                "address chooser",
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().descriptionStartsWith("Home")',
            )

        time.sleep(WAIT_POLL_INTERVAL)

    raise TimeoutException("Timed out waiting for the expected registration state")


def get_edit_text(index, timeout=10):
    return build_wait(timeout).until(
        EC.presence_of_element_located(
            (
                AppiumBy.ANDROID_UIAUTOMATOR,
                f'new UiSelector().className("android.widget.EditText").instance({index})',
            )
        )
    )


def get_visible_edit_texts_now():
    elements = driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.EditText")
    visible = []

    for element in elements:
        try:
            if element.is_displayed():
                visible.append(element)
        except StaleElementReferenceException:
            continue

    return visible


def get_visible_edit_texts(timeout=10, min_count=1):
    def _visible_inputs(_driver):
        visible = get_visible_edit_texts_now()
        return visible if len(visible) >= min_count else False

    return build_wait(timeout).until(_visible_inputs)


def get_visible_edit_texts_count(timeout=10, min_count=1):
    return len(get_visible_edit_texts(timeout=timeout, min_count=min_count))


def has_home_address_card():
    return (
        get_first_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().descriptionStartsWith("Home")',
        )
        is not None
    )


def log_duration(label, started_at):
    print(f"⏱️ {label}: {time.perf_counter() - started_at:.2f}s")


def read_field_value(field):
    return (
        field.get_attribute("text")
        or field.get_attribute("contentDescription")
        or field.text
        or ""
    ).strip()


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
    handled = False

    if click_if_present(AppiumBy.ACCESSIBILITY_ID, "Enable Location", PERMISSION_WAIT_TIMEOUT):
        handled = True
        safe_click(
            AppiumBy.ID,
            "com.android.permissioncontroller:id/permission_allow_foreground_only_button",
            PERMISSION_WAIT_TIMEOUT,
        )

    if click_if_present(
        AppiumBy.ACCESSIBILITY_ID,
        "Enable Notification",
        PERMISSION_WAIT_TIMEOUT,
    ):
        handled = True
        safe_click(
            AppiumBy.ID,
            "com.android.permissioncontroller:id/permission_allow_button",
            PERMISSION_WAIT_TIMEOUT,
        )

    for by, value in (
        (
            AppiumBy.ID,
            "com.android.permissioncontroller:id/permission_allow_button",
        ),
        (
            AppiumBy.ID,
            "com.android.permissioncontroller:id/permission_allow_foreground_only_button",
        ),
    ):
        if click_if_present(by, value, PERMISSION_WAIT_TIMEOUT):
            handled = True

    return handled


def handle_intro_templates():
    if click_if_present(AppiumBy.ACCESSIBILITY_ID, "Got it! Thanks", INTRO_WAIT_TIMEOUT):
        print("✅ Clicked 'Got it! Thanks'")
        return True

    if click_if_present(AppiumBy.ACCESSIBILITY_ID, "Order Now", INTRO_WAIT_TIMEOUT):
        print("✅ Clicked 'Order Now'")
        return True

    return False


# ------------------------------------------
# Helper: Login / OTP
# ------------------------------------------
def enter_mobile_number():
    print("📲 Entering phone number and waiting for OTP screen...")
    started_at = time.perf_counter()

    for attempt in range(1, PHONE_ENTRY_ATTEMPT_MAX + 1):
        mobile_input = wait.until(
            EC.element_to_be_clickable((AppiumBy.CLASS_NAME, "android.widget.EditText"))
        )
        mobile_input.click()
        mobile_input.clear()
        mobile_input.send_keys(PHONE_NUMBER)

        continue_button = wait.until(
            EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Continue"))
        )
        continue_button.click()

        state = wait_for_phone_to_otp_transition()
        if state == "otp":
            print(f"✅ OTP screen opened after phone entry (attempt {attempt})")
            log_duration("Phone number entry", started_at)
            return

        print(
            f"⚠️ App returned to phone entry state after clicking Continue (attempt {attempt})"
        )
        log_screen_state(f"phone entry retry {attempt}")
        handle_permissions()
        time.sleep(FIELD_RETRY_DELAY)

    raise TimeoutException("Phone number entry did not advance to OTP screen")


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

    end_time = time.perf_counter() + OTP_VERIFY_TIMEOUT

    while time.perf_counter() < end_time:
        for label, by, value in selectors:
            if click_if_present(by, value, 0):
                print(f"✅ Verify button clicked via {label}")
                return True

        time.sleep(WAIT_POLL_INTERVAL)

    return False


def wait_for_phone_to_otp_transition(timeout=PHONE_TO_OTP_TIMEOUT):
    end_time = time.perf_counter() + timeout

    while time.perf_counter() < end_time:
        if is_present(AppiumBy.ACCESSIBILITY_ID, "Verify", 0):
            return "otp"

        if is_present(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().text("Verify")',
            0,
        ):
            return "otp"

        if is_present(AppiumBy.ACCESSIBILITY_ID, "Continue", 0) and len(
            get_visible_edit_texts_now()
        ) == 1:
            return "phone"

        time.sleep(WAIT_POLL_INTERVAL)

    return "unknown"


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
    started_at = time.perf_counter()

    for attempt in range(1, OTP_ATTEMPT_MAX + 1):
        try:
            driver.activate_app(APP_PACKAGE)
            time.sleep(UI_SETTLE_DELAY)

            otp_input = wait.until(
                EC.element_to_be_clickable((AppiumBy.CLASS_NAME, "android.widget.EditText"))
            )
            otp_input.click()
            time.sleep(UI_SETTLE_DELAY)

            try:
                otp_input.clear()
            except Exception:
                pass

            run_adb_command(["shell", "input", "text", otp])
            time.sleep(UI_SETTLE_DELAY)
            field_value = read_field_value(otp_input)
            print(
                f"⌨️ Fixed OTP typed via ADB (attempt {attempt}) | "
                f"field snapshot: {field_value or '<masked/empty>'}"
            )
            log_screen_state(f"after OTP entry attempt {attempt}")

            if not find_and_click_verify_button():
                print(f"⚠️ Verify button not found after OTP entry (attempt {attempt})")
                log_screen_state("verify button not found")
                time.sleep(FIELD_RETRY_DELAY)
                continue

            label = wait_for_post_otp_state()
            if label == "profile screen" or label == "home screen":
                print("✅ OTP flow completed to logged-in state")
            log_duration("OTP verification flow", started_at)
            return True

        except Exception as error:
            print(f"⚠️ Error while entering OTP (attempt {attempt}): {error}")
            log_screen_state(f"OTP attempt {attempt} failed")

        time.sleep(FIELD_RETRY_DELAY)

    raise Exception("❌ Failed to move past OTP screen after multiple attempts")


# ------------------------------------------
# Helper: Registration flow
# ------------------------------------------
def fill_name():
    started_at = time.perf_counter()
    name_input = wait.until(
        EC.element_to_be_clickable(
            (
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().className("android.widget.EditText").instance(0)',
            )
        )
    )
    name_input.click()
    name_input.clear()
    name_input.send_keys(CUSTOMER_NAME)

    driver.execute_script("mobile:pressKey", {"keycode": 4})

    next_button = wait.until(EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Next")))
    next_button.click()
    print("✅ Name entered successfully")
    log_duration("Customer name entry", started_at)


def click_delivery_location_result():
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

    end_time = time.perf_counter() + SEARCH_RESULT_TIMEOUT

    while time.perf_counter() < end_time:
        for label, by, value in result_selectors:
            if click_if_present(by, value, 0):
                print(f"✅ Selected delivery location via {label}: {DELIVERY_LOCATION_RESULT}")
                return True

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
                return True
            except StaleElementReferenceException:
                continue

        time.sleep(WAIT_POLL_INTERVAL)

    return False


def select_delivery_location():
    print(f"📍 Searching delivery location: {DELIVERY_LOCATION_QUERY}")
    started_at = time.perf_counter()

    click_if_present(AppiumBy.ACCESSIBILITY_ID, "Enter location manually", INTRO_WAIT_TIMEOUT)

    search_box = build_wait(SEARCH_RESULT_TIMEOUT).until(
        EC.element_to_be_clickable((AppiumBy.CLASS_NAME, "android.widget.EditText"))
    )
    search_box.click()
    search_box.clear()
    search_box.send_keys(DELIVERY_LOCATION_QUERY)

    if not click_delivery_location_result():
        print("⚠️ Delivery location result for Bus stand Khopoli was not found")
        return False

    confirm_button = build_wait(LOCATION_CONFIRM_TIMEOUT).until(
        EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Confirm Location"))
    )
    confirm_button.click()
    print("✅ Confirmed delivery location")

    build_wait(LOCATION_CONFIRM_TIMEOUT).until(
        EC.any_of(
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Confirm Address")),
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Next")),
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Add Address")),
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Profile")),
        )
    )
    log_duration("Delivery location selection", started_at)
    return True


def fill_two_line_address(line_1, line_2, label):
    started_at = time.perf_counter()
    build_wait(LOCATION_CONFIRM_TIMEOUT).until(
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
                time.sleep(UI_SETTLE_DELAY)
                field.clear()
                field.send_keys(value)
                time.sleep(UI_SETTLE_DELAY)

                entered_value = read_field_value(field)

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

            time.sleep(FIELD_RETRY_DELAY)

        raise TimeoutException(f"Failed to enter value for {field_label}")

    type_and_verify(first_input, line_1, "House / Flat Number")
    type_and_verify(second_input, line_2, "Tower / Building Name")

    driver.execute_script("mobile:pressKey", {"keycode": 4})
    time.sleep(UI_SETTLE_DELAY)

    confirm_address = wait.until(
        EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Confirm Address"))
    )
    confirm_address.click()
    print(f"✅ {label} entered successfully")
    log_duration("Address details entry", started_at)


def open_add_address_if_needed():
    if click_if_present(AppiumBy.ACCESSIBILITY_ID, "Add Address", FAST_CHECK_TIMEOUT):
        print("✅ Clicked 'Add Address'")
        return True

    if has_home_address_card():
        home_card = driver.find_elements(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().descriptionStartsWith("Home")',
        )[0]
        home_card.click()
        print("✅ Opened address chooser")
        safe_click(AppiumBy.ACCESSIBILITY_ID, "Add Address", INTRO_WAIT_TIMEOUT)
        return True

    return False


def detect_registration_state(timeout=STATE_CHECK_TIMEOUT):
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

    try:
        label, _, _ = get_first_present_locator(locator_groups, timeout=timeout)
        return label
    except TimeoutException:
        return None


def finish_registration():
    delivery_location_done = False
    name_done = False
    address_details_done = False

    for _ in range(12):
        if handle_permissions():
            time.sleep(FLOW_SETTLE_DELAY)
            continue

        state = detect_registration_state()

        if state == "profile screen":
            print("✅ Registration flow reached profile/home state")
            return

        if state == "delivery location" and not delivery_location_done:
            if not select_delivery_location():
                log_screen_state("delivery location suggestion missing")
                raise Exception("❌ Delivery location suggestions were not available")
            delivery_location_done = True
            time.sleep(FLOW_SETTLE_DELAY)
            continue

        if state == "delivery location" and delivery_location_done:
            print("⏳ Waiting for delivery location screen to transition after confirmation...")
            time.sleep(FIELD_RETRY_DELAY)
            continue

        if state == "address form" and not address_details_done:
            print("📝 Address detail form detected")
            fill_two_line_address(
                ADDRESS_LINE_1,
                ADDRESS_LINE_2,
                "address details",
            )
            address_details_done = True
            time.sleep(FLOW_SETTLE_DELAY)
            continue

        if state in ("address add button", "address chooser") and not address_details_done and open_add_address_if_needed():
            time.sleep(FLOW_SETTLE_DELAY)
            continue

        if state == "name step" and not name_done:
            fill_name()
            name_done = True
            time.sleep(FLOW_SETTLE_DELAY)
            continue

        if state in ("intro screen", "home screen") and handle_intro_templates():
            time.sleep(FLOW_SETTLE_DELAY)
            continue

        if state == "profile screen":
            print("✅ Registration flow reached profile/home state")
            return

        log_screen_state("unexpected registration state")
        time.sleep(FIELD_RETRY_DELAY)

    raise Exception("❌ Registration flow did not reach the home/profile screen")


# ------------------------------------------
# Helper: Profile / logout
# ------------------------------------------
def open_profile():
    started_at = time.perf_counter()
    if safe_click(AppiumBy.ACCESSIBILITY_ID, "Profile", PROFILE_WAIT_TIMEOUT):
        log_duration("Profile open", started_at)
        return

    if safe_click(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.widget.ImageView").instance(8)',
        INTRO_WAIT_TIMEOUT,
    ):
        log_duration("Profile open", started_at)
        return

    log_screen_state("profile button not found")
    raise TimeoutException("Profile button was not available")


def logout_user():
    safe_click(AppiumBy.ACCESSIBILITY_ID, "Sign out", 10)
    safe_click(AppiumBy.ACCESSIBILITY_ID, "Sign Out", 10)
    print("✅ Logout completed successfully")


def wait_for_login_entry_state():
    build_wait(12).until(
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
    safe_click(AppiumBy.ACCESSIBILITY_ID, "LogIn", 2)
    handle_permissions()
    enter_mobile_number()
    enter_otp_safely(FIXED_OTP)
    handle_permissions()
    handle_intro_templates()
    build_wait(12).until(
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

    build_wait(12).until(
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
    driver.implicitly_wait(0)
    wait = build_wait(40)
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
