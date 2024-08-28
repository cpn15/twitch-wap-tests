import os
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException,\
      TimeoutException, ElementClickInterceptedException
from config.Data import Data


class Page:

    SCREENSHOT_PATH = 'screenshots/'

    def __init__(self,driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self.action = ActionChains(self.driver)

    def wait_for(self, locator):
        """Waits for the presence of an element via a locator."""
        return self.wait.until(EC.presence_of_element_located(locator))

    def wait_before_click(self,locator):
        """Locates an element and provides stability before click action"""
        self.wait.until(EC.presence_of_element_located(locator))
        return self.wait.until(EC.element_to_be_clickable(locator))
    
    def scroll_down(self, times):
        """Scrolls down the page with the number of times provided"""
        body = self.driver.find_element(By.TAG_NAME, 'body')
        for _ in range(times):
            body.send_keys(Keys.PAGE_DOWN)
        return self

    def click_element(self, element):
        """Click an element using JavaScript if regular click fails."""
        try:
            element.click()
        except (TimeoutException, NoSuchElementException,\
                 ElementClickInterceptedException):
            self.driver.execute_script("arguments[0].click();", element)

    def scroll_to_element(self, element):
        """Scroll the element into view using JavaScript."""
        self.driver.execute_script(\
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)

    def generate_screenshot_filename(self):
        """Generate a unique filename for the screenshot with a timestamp."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        return os.path.join(self.SCREENSHOT_PATH, \
                            f"{Data.DEVICE_NAME}_{Data.LIVE_GAME}_{timestamp}.png")

    def take_screenshot(self):
        """Take a screenshot of the current page."""
        try:
            screenshot_dir = self.generate_screenshot_filename()
            os.makedirs(self.SCREENSHOT_PATH, exist_ok=True)
            self.driver.get_screenshot_as_file(screenshot_dir)
        except Exception as e:
            print(f"Error while taking screenshot: {e}")
