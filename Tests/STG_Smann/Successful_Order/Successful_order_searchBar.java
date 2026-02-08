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
    WebElement el175 = driver.findElement(AppiumBy.className("android.widget.EditText"));
    el175.click();
    el175.sendKeys("9999999999");
    WebElement el176 = driver.findElement(AppiumBy.accessibilityId("Continue"));
    el176.click();
    WebElement el177 = driver.findElement(AppiumBy.className("android.widget.EditText"));
    el177.click();
    el177.sendKeys("1234");
    WebElement el178 = driver.findElement(AppiumBy.accessibilityId("Search “Pizza”"));
    el178.click();
    WebElement el179 = driver.findElement(AppiumBy.className("android.widget.EditText"));
    el179.click();
    el179.sendKeys("samosa");
    WebElement el180 = driver.findElement(AppiumBy.androidUIAutomator("new UiSelector().className(\"android.widget.ImageView\").instance(1)"));
    el180.click();
    WebElement el181 = driver.findElement(AppiumBy.androidUIAutomator("new UiSelector().description(\"CHOLE SAMOSA FUSION\n₹ 75.00\")"));
    el181.click();
    WebElement el182 = driver.findElement(AppiumBy.androidUIAutomator("new UiSelector().description(\"Add\").instance(0)"));
    el182.click();
    WebElement el183 = driver.findElement(AppiumBy.androidUIAutomator("new UiSelector().description(\"Add\").instance(0)"));
    el183.click();
    WebElement el184 = driver.findElement(AppiumBy.androidUIAutomator("new UiSelector().className(\"android.widget.Button\").instance(3)"));
    el184.click();
    WebElement el185 = driver.findElement(AppiumBy.accessibilityId("3 items added"));
    el185.click();
    WebElement el186 = driver.findElement(AppiumBy.androidUIAutomator("new UiSelector().description(\"₹180.00\nTotal\nPlace Order\")"));
    el186.click();
    WebElement el187 = driver.findElement(AppiumBy.androidUIAutomator("new UiSelector().className(\"android.widget.ImageView\").instance(10)"));
    el187.click();
    WebElement el188 = driver.findElement(AppiumBy.androidUIAutomator("new UiSelector().description(\"test\nNew\n#4122\n2 Items\n02 Feb 26 05:15 PM\n₹ 180.00\nCASH\nSUBMITTED\nDELIVERY\nDetails\")"));
    el188.click();
    WebElement el189 = driver.findElement(AppiumBy.androidUIAutomator("new UiSelector().className(\"android.view.View\").instance(7)"));
    el189.click();
    WebElement el190 = driver.findElement(AppiumBy.androidUIAutomator("new UiSelector().className(\"android.widget.ImageView\").instance(13)"));
    el190.click();
    WebElement el191 = driver.findElement(AppiumBy.accessibilityId("Sign out"));
    el191.click();
    WebElement el192 = driver.findElement(AppiumBy.accessibilityId("Sign Out"));
    el192.click();
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
