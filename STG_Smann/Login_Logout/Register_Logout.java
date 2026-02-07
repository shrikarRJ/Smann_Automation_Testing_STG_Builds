// This sample code supports Appium Java client >=9
// https://github.com/appium/java-client
import io.appium.java_client.remote.options.BaseOptions;
import io.appium.java_client.AppiumBy;
import io.appium.java_client.android.AndroidDriver;
import java.net.URL;
import java.net.MalformedURLException;
import java.time.Duration;
import java.util.Arrays;
import java.util.Base64;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.openqa.selenium.*;

public class SampleTest {

  private AndroidDriver driver;

  @Before
  public void setUp() {
    Capabilities options = new BaseOptions()
      .amend("platformName", "Android")
      .amend("appium:automationName", "UiAutomator2")
      .amend("appium:deviceName", "emulator-5554")
      .amend("appium:app", "C:\\Users\\shrik\\OneDrive\\Desktop\\Smann_TBT\\Smann_STG_APK\\STG_Smann.apk")
      .amend("appium:appPackage", "com.tribetayling.customer.staging")
      .amend("appium:appActivity", "com.tribetayling.customer.MainActivity")
      .amend("appium:fullReset", true)
      .amend("appium:newCommandTimeout", 300)
      .amend("appium:ensureWebviewsHavePages", true)
      .amend("appium:nativeWebScreenshot", true)
      .amend("appium:connectHardwareKeyboard", true);    

    driver = new AndroidDriver(this.getUrl(), options);
  }

  @Test
  public void sampleTest() {
    WebElement el1 = driver.findElement(AppiumBy.className("android.widget.EditText"));
    el1.click();
    el1.sendKeys("9021004607");
    WebElement el2 = driver.findElement(AppiumBy.accessibilityId("Continue"));
    el2.click();
    WebElement el3 = driver.findElement(AppiumBy.className("android.widget.EditText"));
    el3.click();
    el3.sendKeys("7888");
    WebElement el4 = driver.findElement(AppiumBy.id("com.android.permissioncontroller:id/permission_allow_foreground_only_button"));
    el4.click();
    WebElement el5 = driver.findElement(AppiumBy.androidUIAutomator("new UiSelector().className(\"android.widget.EditText\").instance(0)"));
    el5.click();
    el5.sendKeys("Shrikar Jagtap");
    driver.executeScript("mobile:pressKey", Map.ofEntries(Map.entry("keycode", 4)));
    WebElement el6 = driver.findElement(AppiumBy.accessibilityId("Next"));
    el6.click();
    WebElement el7 = driver.findElement(AppiumBy.androidUIAutomator("new UiSelector().className(\"android.widget.EditText\").instance(0)"));
    el7.click();
    el7.sendKeys("Flat 312, Floor 3 ");
    WebElement el8 = driver.findElement(AppiumBy.androidUIAutomator("new UiSelector().className(\"android.widget.EditText\").instance(1)"));
    el8.click();
    el8.sendKeys("Tower C, Sector 5");
    driver.executeScript("mobile:pressKey", Map.ofEntries(Map.entry("keycode", 4)));
    WebElement el9 = driver.findElement(AppiumBy.accessibilityId("Confirm Address"));
    el9.click();
    WebElement el10 = driver.findElement(AppiumBy.androidUIAutomator("new UiSelector().description(\"Get 25% OFF on Your First Order\nGet 25% off up to Rs. 25 on a minimum order value of Rs. 199.\nDon't Miss Out - Shop Now & Save BIG !!\")"));
    el10.click();
    WebElement el11 = driver.findElement(AppiumBy.accessibilityId("Got it! Thanks"));
    el11.click();
    WebElement el12 = driver.findElement(AppiumBy.androidUIAutomator("new UiSelector().className(\"android.widget.ImageView\").instance(8)"));
    el12.click();
    WebElement el13 = driver.findElement(AppiumBy.accessibilityId("Sign out"));
    el13.click();
    WebElement el14 = driver.findElement(AppiumBy.accessibilityId("Sign Out"));
    el14.click();
  }

  @After
  public void tearDown() {
    driver.quit();
  }

  private URL getUrl() {
      try {
        return new URL("http://127.0.0.1:4723");
      } catch (MalformedURLException e) {
        e.printStackTrace();
      }
    }
}
