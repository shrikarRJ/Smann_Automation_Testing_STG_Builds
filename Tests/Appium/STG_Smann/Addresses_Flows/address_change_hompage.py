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
PHONE_NUMBER = "9999990102"
FIXED_OTP = "1234"
NEW_ADDRESS_LINE_1 = "0102"
NEW_ADDRESS_LINE_2 = "test customer"
DELIVERY_LOCATION_QUERY = "Khopoli bus stand"
DELIVERY_LOCATION_RESULT = (
    "Khopoli ST Bus Stand, Laxminagar, Khopoli, Maharashtra, India"
)

TEMP_ADDRESS_KEYWORDS = ("0102", "test customer", "Khopoli ST Bus Stand")
ORIGINAL_ADDRESS_KEYWORDS = ("001", "Washi")

DEVICE_UDID = "ZA222KCFFQ"

APK_PATH = os.environ.get(
    "APK_PATH",
    r"C:\Users\shrik\OneDrive\Desktop\Smann_Automation_Testing_STG_Builds\Tests\Appium\STG_Smann\Smann_STG_APK\STG_Smann.apk",
)

APP_PACKAGE = "com.tribetayling.customer.staging"
APP_ACTIVITY = "com.tribetayling.customer.MainActivity"
APPIUM_SERVER_URL = "http://127.0.0.1:4723"

WAIT_POLL_INTERVAL = 0.2
FIELD_RETRY_DELAY = 0.3
UI_SETTLE_DELAY = 0.2
FLOW_SETTLE_DELAY = 0.5
FAST_CHECK_TIMEOUT = 0.8
PHONE_TO_OTP_TIMEOUT = 8
OTP_ATTEMPT_MAX = 3
OTP_VERIFY_TIMEOUT = 12
POST_OTP_STATE_TIMEOUT = 20
PERMISSION_WAIT_TIMEOUT = 1.2
INTRO_WAIT_TIMEOUT = 1.0
SEARCH_RESULT_TIMEOUT = 8
LOCATION_CONFIRM_TIMEOUT = 15
PROFILE_WAIT_TIMEOUT = 6
HOME_READY_TIMEOUT = 20
ADDRESS_CARD_TIMEOUT = 10
DELETE_ACTION_TIMEOUT = 5

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
        print("[INFO] App not found on device. Installing APK...")
        run_adb_command(["install", "-r", APK_PATH])
        print("[OK] App installed")
    else:
        print("[OK] App already installed on device")


def reset_app_storage():
    print("[INFO] Clearing app data before test run...")
    run_adb_command(["shell", "am", "force-stop", APP_PACKAGE], check=False)
    result = run_adb_command(["shell", "pm", "clear", APP_PACKAGE], check=False)

    clear_output = f"{result.stdout}\n{result.stderr}".strip()
    if "Success" not in clear_output:
        raise RuntimeError(f"Failed to clear app data: {clear_output}")

    print("[OK] App data cleared")


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


def read_field_value(field):
    return (
        field.get_attribute("text")
        or field.get_attribute("contentDescription")
        or field.text
        or ""
    ).strip()


def normalize_text(value):
    return " ".join((value or "").split()).strip().lower()


def element_text(element):
    return (
        element.get_attribute("contentDescription")
        or element.get_attribute("text")
        or element.text
        or ""
    ).strip()


def log_screen_state(label):
    print(f"[DEBUG] Screen state: {label}")
    snapshots = []

    for by, locator in (
        (AppiumBy.XPATH, "//*[@content-desc]"),
        (AppiumBy.XPATH, "//*[@text]"),
    ):
        try:
            for element in driver.find_elements(by, locator)[:10]:
                value = element_text(element)
                if value:
                    snapshots.append(value)
        except Exception:
            continue

    if snapshots:
        print("        Visible elements:", " | ".join(dict.fromkeys(snapshots)))
    else:
        print("        Visible elements: <not captured>")


def matches_keywords(value, keywords):
    normalized = normalize_text(value)
    return all(normalize_text(keyword) in normalized for keyword in keywords)


def find_visible_element_by_keywords(keywords, timeout=0):
    end_time = time.perf_counter() + max(timeout, 0)

    while True:
        try:
            candidates = driver.find_elements(AppiumBy.XPATH, "//*[@content-desc or @text]")
        except Exception:
            candidates = []

        for element in candidates:
            try:
                if not element.is_displayed():
                    continue
                value = element_text(element)
                if value and matches_keywords(value, keywords):
                    return element, value
            except StaleElementReferenceException:
                continue

        if timeout <= 0 or time.perf_counter() >= end_time:
            return None, None

        time.sleep(WAIT_POLL_INTERVAL)


def click_visible_element_by_keywords(keywords, timeout, label):
    end_time = time.perf_counter() + timeout

    while time.perf_counter() < end_time:
        element, value = find_visible_element_by_keywords(keywords, 0)
        if element is None:
            time.sleep(WAIT_POLL_INTERVAL)
            continue

        try:
            element.click()
            print(f"[OK] Clicked {label}: {value}")
            return value
        except StaleElementReferenceException:
            time.sleep(WAIT_POLL_INTERVAL)
        except Exception as error:
            print(f"[WARN] Failed clicking {label}: {error}")
            time.sleep(WAIT_POLL_INTERVAL)

    raise TimeoutException(f"Could not find {label} matching {keywords}")


def has_home_address_card():
    return (
        get_first_element(
            AppiumBy.ANDROID_UIAUTOMATOR,
            'new UiSelector().descriptionStartsWith("Home")',
        )
        is not None
    )


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
        print("[OK] Clicked 'Got it! Thanks'")
        return True

    if click_if_present(AppiumBy.ACCESSIBILITY_ID, "Order Now", INTRO_WAIT_TIMEOUT):
        print("[OK] Clicked 'Order Now'")
        return True

    return False


def wait_for_homepage_ready():
    end_time = time.perf_counter() + HOME_READY_TIMEOUT

    while time.perf_counter() < end_time:
        if handle_permissions():
            time.sleep(FLOW_SETTLE_DELAY)
            continue

        if handle_intro_templates():
            time.sleep(FLOW_SETTLE_DELAY)
            continue

        if has_home_address_card():
            print("[OK] Homepage is ready")
            return

        if is_present(AppiumBy.ACCESSIBILITY_ID, "Profile", 0):
            time.sleep(FLOW_SETTLE_DELAY)
            continue

        time.sleep(WAIT_POLL_INTERVAL)

    log_screen_state("homepage ready timeout")
    raise TimeoutException("Homepage did not become ready")


# ------------------------------------------
# Helper: Login / OTP
# ------------------------------------------
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


def enter_mobile_number():
    print("[INFO] Entering phone number and waiting for OTP screen...")

    for attempt in range(1, 4):
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
            print(f"[OK] OTP screen opened after phone entry (attempt {attempt})")
            return

        print(f"[WARN] Still on phone entry screen after attempt {attempt}")
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
                print(f"[OK] Verify button clicked via {label}")
                return True

        time.sleep(WAIT_POLL_INTERVAL)

    return False


def get_first_present_locator(locator_groups, timeout=POST_OTP_STATE_TIMEOUT):
    end_time = time.perf_counter() + timeout

    while time.perf_counter() < end_time:
        for label, by, value in locator_groups:
            if is_present(by, value, 0):
                return label

        if has_home_address_card():
            return "home address"

        time.sleep(WAIT_POLL_INTERVAL)

    raise TimeoutException("Timed out waiting for the expected post-OTP state")


def wait_for_post_otp_state():
    locator_groups = (
        ("location permission", AppiumBy.ACCESSIBILITY_ID, "Enable Location"),
        ("notification permission", AppiumBy.ACCESSIBILITY_ID, "Enable Notification"),
        ("intro screen", AppiumBy.ACCESSIBILITY_ID, "Got it! Thanks"),
        ("home screen", AppiumBy.ACCESSIBILITY_ID, "Order Now"),
        ("profile screen", AppiumBy.ACCESSIBILITY_ID, "Profile"),
    )

    label = get_first_present_locator(locator_groups)
    print(f"[OK] Post-OTP state detected: {label}")
    return label


def enter_otp_safely(otp):
    print("[INFO] Entering fixed OTP safely...")

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
                f"[INFO] OTP typed via ADB (attempt {attempt}) | "
                f"field snapshot: {field_value or '<masked/empty>'}"
            )

            if not find_and_click_verify_button():
                print(f"[WARN] Verify button not found after OTP entry (attempt {attempt})")
                log_screen_state("verify button not found")
                time.sleep(FIELD_RETRY_DELAY)
                continue

            wait_for_post_otp_state()
            return True

        except Exception as error:
            print(f"[WARN] Error while entering OTP (attempt {attempt}): {error}")
            log_screen_state(f"otp attempt {attempt} failed")

        time.sleep(FIELD_RETRY_DELAY)

    raise Exception("Failed to move past OTP screen after multiple attempts")


# ------------------------------------------
# Helper: Homepage address flow
# ------------------------------------------
def open_address_chooser():
    wait_for_homepage_ready()

    for attempt in range(1, 4):
        if has_home_address_card():
            home_card = driver.find_elements(
                AppiumBy.ANDROID_UIAUTOMATOR,
                'new UiSelector().descriptionStartsWith("Home")',
            )[0]
            home_card.click()
        else:
            click_visible_element_by_keywords(
                ORIGINAL_ADDRESS_KEYWORDS,
                ADDRESS_CARD_TIMEOUT,
                "homepage address card",
            )

        if is_present(AppiumBy.ACCESSIBILITY_ID, "Add Address", 2):
            print(f"[OK] Opened address chooser (attempt {attempt})")
            return

        time.sleep(FLOW_SETTLE_DELAY)

    log_screen_state("address chooser did not open")
    raise TimeoutException("Address chooser did not open after tapping the home address card")


def is_address_chooser_open():
    return is_present(AppiumBy.ACCESSIBILITY_ID, "Add Address", 0)


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
                print(f"[OK] Selected delivery location via {label}")
                return True

        suggestions = driver.find_elements(AppiumBy.XPATH, "//*[@text or @content-desc]")
        for suggestion in suggestions:
            try:
                description = element_text(suggestion)
            except StaleElementReferenceException:
                continue

            if "khopoli st bus stand" not in normalize_text(description):
                continue

            try:
                suggestion.click()
                print(f"[OK] Selected delivery location from visible suggestions: {description}")
                return True
            except StaleElementReferenceException:
                continue

        time.sleep(WAIT_POLL_INTERVAL)

    return False


def select_delivery_location():
    print(f"[INFO] Searching delivery location: {DELIVERY_LOCATION_QUERY}")

    click_if_present(AppiumBy.ACCESSIBILITY_ID, "Enter location manually", INTRO_WAIT_TIMEOUT)

    search_box = build_wait(SEARCH_RESULT_TIMEOUT).until(
        EC.element_to_be_clickable((AppiumBy.CLASS_NAME, "android.widget.EditText"))
    )
    search_box.click()
    search_box.clear()
    search_box.send_keys(DELIVERY_LOCATION_QUERY)

    if not click_delivery_location_result():
        print("[WARN] Delivery location result was not found")
        return False

    confirm_button = build_wait(LOCATION_CONFIRM_TIMEOUT).until(
        EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Confirm Location"))
    )
    confirm_button.click()
    print("[OK] Confirmed delivery location")

    build_wait(LOCATION_CONFIRM_TIMEOUT).until(
        EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Confirm Address"))
    )
    return True


def fill_address_details():
    print("[INFO] Filling homepage address details...")

    # The location search box can still be visible above the address form.
    # Use the last 3 visible inputs as the address fields, then fill the first
    # 2 mandatory fields: House No. & Floor and Building & Block No.
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
                    print(f"[OK] {field_label} entered: {entered_value}")
                    return

                print(
                    f"[WARN] {field_label} value not confirmed on attempt {attempt}. "
                    f"Read back: {entered_value or '<empty>'}"
                )
            except StaleElementReferenceException:
                refreshed_inputs = get_visible_edit_texts(timeout=5, min_count=3)[-3:]
                field = refreshed_inputs[0] if field_label == "House / Flat Number" else refreshed_inputs[1]
            except Exception as error:
                print(f"[WARN] Error entering {field_label} on attempt {attempt}: {error}")

            time.sleep(FIELD_RETRY_DELAY)

        raise TimeoutException(f"Failed to enter value for {field_label}")

    type_and_verify(first_input, NEW_ADDRESS_LINE_1, "House / Flat Number")
    driver.execute_script("mobile:pressKey", {"keycode": 4})
    time.sleep(UI_SETTLE_DELAY)

    type_and_verify(second_input, NEW_ADDRESS_LINE_2, "Tower / Building Name")
    driver.execute_script("mobile:pressKey", {"keycode": 4})
    time.sleep(UI_SETTLE_DELAY)

    confirm_address = wait.until(
        EC.element_to_be_clickable((AppiumBy.ACCESSIBILITY_ID, "Confirm Address"))
    )
    confirm_address.click()
    print("[OK] Address details confirmed")


def dismiss_post_address_prompt_if_present():
    if click_if_present(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.widget.Button").instance(0)',
        FAST_CHECK_TIMEOUT,
    ):
        print("[OK] Dismissed post-address prompt")
        time.sleep(FLOW_SETTLE_DELAY)


def select_temporary_home_address():
    click_visible_element_by_keywords(
        TEMP_ADDRESS_KEYWORDS,
        ADDRESS_CARD_TIMEOUT,
        "temporary homepage address",
    )
    time.sleep(FLOW_SETTLE_DELAY)


def wait_for_active_home_address(keywords, label):
    end_time = time.perf_counter() + ADDRESS_CARD_TIMEOUT

    while time.perf_counter() < end_time:
        if is_present(AppiumBy.ACCESSIBILITY_ID, "Add Address", 0):
            time.sleep(WAIT_POLL_INTERVAL)
            continue

        element, value = find_visible_element_by_keywords(keywords, 0)
        if element is not None:
            print(f"[OK] Active homepage address confirmed for {label}: {value}")
            return value

        time.sleep(WAIT_POLL_INTERVAL)

    raise TimeoutException(f"Active homepage address was not updated for {label}")


def return_to_homepage_from_address_section():
    for attempt in range(1, 4):
        if not is_address_chooser_open():
            if has_home_address_card() or is_present(AppiumBy.ACCESSIBILITY_ID, "Profile", 0):
                print("[OK] Returned to homepage from address section")
                return
        else:
            driver.execute_script("mobile:pressKey", {"keycode": 4})
            print(f"[INFO] Back navigation used to return from address section (attempt {attempt})")
            time.sleep(FLOW_SETTLE_DELAY)

        if handle_permissions():
            time.sleep(FLOW_SETTLE_DELAY)
            continue

        if handle_intro_templates():
            time.sleep(FLOW_SETTLE_DELAY)
            continue

        time.sleep(WAIT_POLL_INTERVAL)

    wait_for_homepage_ready()


def add_and_select_new_homepage_address():
    open_address_chooser()

    if not safe_click(AppiumBy.ACCESSIBILITY_ID, "Add Address", ADDRESS_CARD_TIMEOUT):
        raise TimeoutException("'Add Address' was not available")

    print("[OK] Clicked 'Add Address'")

    if not select_delivery_location():
        log_screen_state("delivery location search failed")
        raise TimeoutException("Delivery location suggestions were not available")

    fill_address_details()
    dismiss_post_address_prompt_if_present()
    select_temporary_home_address()
    wait_for_active_home_address(TEMP_ADDRESS_KEYWORDS, "temporary homepage address")


def open_selected_address_actions():
    selectors = (
        'new UiSelector().className("android.widget.Button").instance(1)',
        'new UiSelector().className("android.widget.Button").instance(0)',
    )

    for selector in selectors:
        if click_if_present(AppiumBy.ANDROID_UIAUTOMATOR, selector, FAST_CHECK_TIMEOUT):
            print(f"[OK] Opened address action button via selector: {selector}")
            return True

    return False


def confirm_delete_address():
    for label in ("Delete", "DELETE"):
        if safe_click(AppiumBy.ACCESSIBILITY_ID, label, DELETE_ACTION_TIMEOUT):
            print(f"[OK] Clicked delete action via '{label}'")
            break
    else:
        raise TimeoutException("Delete action was not available")

    if not safe_click(AppiumBy.CLASS_NAME, "android.widget.Button", DELETE_ACTION_TIMEOUT):
        raise TimeoutException("Delete confirmation button was not available")

    print("[OK] Address delete confirmed")


def ensure_original_home_address():
    element, value = find_visible_element_by_keywords(ORIGINAL_ADDRESS_KEYWORDS, 0)
    if element is not None and not is_address_chooser_open():
        print(f"[OK] Original homepage address is visible: {value}")
        return

    open_address_chooser()

    for attempt in range(1, 4):
        click_visible_element_by_keywords(
            ORIGINAL_ADDRESS_KEYWORDS,
            ADDRESS_CARD_TIMEOUT,
            f"original homepage address attempt {attempt}",
        )
        time.sleep(FLOW_SETTLE_DELAY)

        if not is_address_chooser_open():
            wait_for_active_home_address(ORIGINAL_ADDRESS_KEYWORDS, "original homepage address")
            return

    log_screen_state("original address selection did not close chooser")
    raise TimeoutException("Failed to set Washi as the active homepage address")


def delete_selected_homepage_address():
    ensure_original_home_address()
    open_address_chooser()

    temp_element, temp_value = find_visible_element_by_keywords(
        TEMP_ADDRESS_KEYWORDS,
        ADDRESS_CARD_TIMEOUT,
    )
    if temp_element is None:
        log_screen_state("temporary address missing before delete")
        raise TimeoutException("Khopoli address was not available for deletion")

    print(f"[OK] Located temporary address for deletion: {temp_value}")

    if not open_selected_address_actions():
        log_screen_state("address action button missing")
        raise TimeoutException("Could not open actions for the selected address")

    confirm_delete_address()
    time.sleep(FLOW_SETTLE_DELAY)

    temp_element, temp_value = find_visible_element_by_keywords(TEMP_ADDRESS_KEYWORDS, 1.5)
    if temp_element is not None and is_address_chooser_open():
        log_screen_state("temporary address still visible after delete")
        raise TimeoutException(f"Khopoli address still appears after delete: {temp_value}")

    ensure_original_home_address()
    return_to_homepage_from_address_section()


# ------------------------------------------
# Helper: Profile / logout
# ------------------------------------------
def open_profile():
    if is_address_chooser_open():
        return_to_homepage_from_address_section()

    wait_for_homepage_ready()

    if safe_click(AppiumBy.ACCESSIBILITY_ID, "Profile", PROFILE_WAIT_TIMEOUT):
        print("[OK] Opened profile")
        return

    if safe_click(
        AppiumBy.ANDROID_UIAUTOMATOR,
        'new UiSelector().className("android.widget.ImageView").instance(8)',
        INTRO_WAIT_TIMEOUT,
    ):
        print("[OK] Opened profile via fallback icon")
        return

    log_screen_state("profile button not found")
    raise TimeoutException("Profile button was not available")


def wait_for_logged_out_state():
    build_wait(12).until(
        EC.any_of(
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "Continue")),
            EC.presence_of_element_located((AppiumBy.ACCESSIBILITY_ID, "LogIn")),
            EC.presence_of_element_located((AppiumBy.CLASS_NAME, "android.widget.EditText")),
        )
    )
    print("[OK] Logged-out state detected")


def logout_user():
    if not safe_click(AppiumBy.ACCESSIBILITY_ID, "Sign out", 10):
        log_screen_state("sign out button missing")
        raise TimeoutException("Sign out button was not available on profile page")

    if not safe_click(AppiumBy.ACCESSIBILITY_ID, "Sign Out", 10):
        log_screen_state("sign out confirmation missing")
        raise TimeoutException("Sign Out confirmation button was not available")

    wait_for_logged_out_state()
    print("[OK] Logout completed successfully")


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

    driver = create_driver()
    driver.implicitly_wait(0)
    wait = build_wait(40)
    print("[OK] App launched successfully")

    handle_permissions()
    enter_mobile_number()
    enter_otp_safely(FIXED_OTP)
    wait_for_homepage_ready()
    add_and_select_new_homepage_address()
    delete_selected_homepage_address()
    open_profile()
    logout_user()


if __name__ == "__main__":
    try:
        main()
    finally:
        if driver is not None:
            time.sleep(2)
            driver.quit()
        print("[OK] Test execution finished")
