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
    WebElement el98 = driver.findElement(AppiumBy.androidUIAutomator("new UiSelector().description(\"India’s #1 Food Delivery \nand Dining App\nLog in or Sign up\n+91 \")"));
    el98.click();
    WebElement el99 = driver.findElement(AppiumBy.className("android.widget.EditText"));
    el99.click();
    el99.sendKeys("9999999999");
    WebElement el100 = driver.findElement(AppiumBy.accessibilityId("Continue"));
    el100.click();
    WebElement el101 = driver.findElement(AppiumBy.className("android.widget.EditText"));
    el101.click();
    el101.sendKeys("1234");
    WebElement el102 = driver.findElement(AppiumBy.accessibilityId("Got it! Thanks"));
    el102.click();
    WebElement el103 = driver.findElement(AppiumBy.accessibilityId("FOOD"));
    el103.click();
    WebElement el104 = driver.findElement(AppiumBy.androidUIAutomator("new UiSelector().description(\"King cafe 222\n20 mins\n0.0 km\")"));
    el104.click();
    WebElement el105 = driver.findElement(AppiumBy.accessibilityId("Menu"));
    el105.click();
    WebElement el106 = driver.findElement(AppiumBy.androidUIAutomator("new UiSelector().description(\"Add\").instance(0)"));
    el106.click();
    WebElement el107 = driver.findElement(AppiumBy.androidUIAutomator("new UiSelector().description(\"Add\").instance(1)"));
    el107.click();
    WebElement el108 = driver.findElement(AppiumBy.androidUIAutomator("new UiSelector().className(\"android.widget.Button\").instance(3)"));
    el108.click();
    WebElement el109 = driver.findElement(AppiumBy.accessibilityId("3 items added"));
    el109.click();
    WebElement el110 = driver.findElement(AppiumBy.androidUIAutomator("new UiSelector().description(\"₹857.66\nTotal\nPlace Order\")"));
    el110.click();
    WebElement el111 = driver.findElement(AppiumBy.androidUIAutomator("new UiSelector().className(\"android.widget.Image\").instance(2)"));
    el111.click();
    WebElement el112 = driver.findElement(AppiumBy.androidUIAutomator("new UiSelector().className(\"android.widget.EditText\").instance(0)"));
    el112.click();
    el112.sendKeys("4100 2800 0000 1007");
    WebElement el113 = driver.findElement(AppiumBy.androidUIAutomator("new UiSelector().className(\"android.widget.EditText\").instance(1)"));
    el113.click();
    el113.sendKeys("0535");
    WebElement el114 = driver.findElement(AppiumBy.androidUIAutomator("new UiSelector().className(\"android.widget.EditText\").instance(2)"));
    el114.sendKeys("136");
    WebElement el115 = driver.findElement(AppiumBy.androidUIAutomator("new UiSelector().resourceId(\"bottom-cta\")"));
    el115.click();
    WebElement el116 = driver.findElement(AppiumBy.androidUIAutomator("new UiSelector().text(\"Maybe later\")"));
    el116.click();
    WebElement el117 = driver.findElement(AppiumBy.androidUIAutomator("new UiSelector().text(\"Success\")"));
    el117.click();
    WebElement el118 = driver.findElement(AppiumBy.androidUIAutomator("new UiSelector().className(\"android.widget.ImageView\").instance(10)"));
    el118.click();
    WebElement el119 = driver.findElement(AppiumBy.androidUIAutomator("new UiSelector().className(\"android.widget.ImageView\").instance(13)"));
    el119.click();
    WebElement el120 = driver.findElement(AppiumBy.accessibilityId("Sign out"));
    el120.click();
    WebElement el121 = driver.findElement(AppiumBy.accessibilityId("Sign Out"));
    el121.click();
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
