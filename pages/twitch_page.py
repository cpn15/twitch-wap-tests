import random
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException, \
    ElementClickInterceptedException
from config.Data import Data
from .common import Page

class TwitchPage(Page):

    SEARCH_ICON  = (By.XPATH, "//a[@aria-label='Search']")
    SEARCH_INPUT = (By.XPATH, "//input[@type='search']")
    MODAL_CLOSE = (By.XPATH, "//button[@data-a-target='modal-close']")
    CHANNELS_SECTION = (By.XPATH, "//h2[text()='CHANNELS']//..//..//../section[1]")
    START_WATCHING_BUTTON = (By.XPATH, "//div[text()='Start Watching']")
    GO_HOME_BUTTON = (By.XPATH, "//div[text()='Go Home']")
    STREAMER_VIDEO = (By.XPATH,"//div[contains(@class, 'default-player') and contains(@class, 'video-player')]")
    VIDEO_PLAYER = (By.XPATH, "//div[@data-a-target='player-overlay-click-handler']")
    STREAMER_INFO = (By.XPATH,"//div[contains(@class, 'streamInfoContainer')]")
    LIVE_STREAMER_NAME = (By.XPATH, "//div[contains(@class, 'streamInfoContainer')]//div[1]/p")
    LIVE_STREAM_INFO = (By.XPATH, "//div[contains(@class, 'streamInfoContainer')]//div[2]/p/a")
    CHAT_BOX = (By.XPATH, "//div[contains(@class, 'chat-scrollable-area__message-container')]")
    PLAYING_BUTTON = (By.XPATH, "//button[@data-a-player-state='playing']")
    STREAMER_NAME = (By.XPATH, "//h3[contains(@class, 'ScTitleText')])[1]")
    FOLLOWERS = (By.XPATH, "//p[text()=' followers']")
    HOME_TAB = (By.XPATH, "//div[text()='Home']")
    ABOUT_TAB = (By.XPATH, "//div[text()='About']")
    SCHEDULE_TAB = (By.XPATH, "//div[text()='Schedule']")
    VIDEOS_TAB = (By.XPATH, "//div[text()='Videos']")
    CLIPS_TAB =  (By.XPATH, "//div[text()='Clips']")
    HOME_VIDEO = (By.XPATH, "//a[contains(@href, 'videos') and contains(@class,'link')]")

    def search_for_a_game(self, game):
        search_icon = self.wait_before_click(self.SEARCH_ICON)
        search_icon.click()
        search_input = self.wait_before_click(self.SEARCH_INPUT)
        search_input.send_keys(game)
        search_input.send_keys(Keys.RETURN)
        return self
    
    def wait_for_search_results_page(self):
        self.wait_for(self.CHANNELS_SECTION)
        return self
    
    def select_random_streamer_from_channels(self):
        max_retries = 3
        retry_delay = 1

        for attempt in range(max_retries):
            try:
                parent_element = self.driver.find_element(*self.CHANNELS_SECTION)
                div_elements = parent_element.find_elements(By.XPATH, "./div")
                total_divs = len(div_elements)

                if total_divs > 1:
                    random_index = random.randint(1, total_divs)
                    random_streamer_xpath = f'//h2[text()="CHANNELS"]\
                        //..//..//../section[1]/div[{random_index}]'
                    
                    clickable_element = self.wait_before_click\
                        ((By.XPATH, random_streamer_xpath))
                    self.scroll_to_element(clickable_element)
                    clickable_element.click()
                    return self
                else:
                    print("Not enough channels to select from.")

            except (TimeoutException, NoSuchElementException, \
                    ElementClickInterceptedException) as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                time.sleep(retry_delay)
        
        raise RuntimeError("Failed to select a random streamer after several attempts.")

    def handle_content_warning(self):
        try:
            start_watching_button = self.wait.until(\
                EC.element_to_be_clickable(self.START_WATCHING_BUTTON))
            start_watching_button.click()

        except (TimeoutException, NoSuchElementException):
            print("No manangement content warning")
        return self

    def handle_popup(self):
        try:
            close_button = self.wait.until(EC.element_to_be_clickable(self.MODAL_CLOSE))
            close_button.click()
        except (TimeoutException, NoSuchElementException) as e:
            print(f"No modal or pop-up found: {e}")
    
    def wait_for_load_and_take_screenshot(self):
        """
        Waits for the page to load and verifies components, then takes a screenshot.

        This method checks for the presence of elements on the live streaming page, such as the video player,
        streamer info, and chat box. It also verifies that the live stream info matches the expected game name.
        If any of these elements are not found within the expected time, the method assumes the page is a
        streamer's profile page and verifies the presence of profile-related components instead.
        """
        try:
            self._verify_live_streaming_page()
        except (TimeoutException, NoSuchElementException):
            try:
                self._verify_streamer_profile_page()
            except (TimeoutException, NoSuchElementException) as e:
                raise RuntimeError(f"Failed to verify page components: {e}")
        
        self.take_screenshot()
        return self
    
    def _verify_live_streaming_page(self):
        """Verifies elements specific to the live streaming page."""
        self.wait_for(self.STREAMER_VIDEO)
        self.wait_for(self.VIDEO_PLAYER)
        self.wait_for(self.STREAMER_INFO)
        self.wait_for(self.LIVE_STREAMER_NAME)
        live_stream_info = self.wait_for(self.LIVE_STREAM_INFO).text
        assert live_stream_info == Data.LIVE_GAME, \
            f"Expected '{Data.LIVE_GAME}', but got '{live_stream_info}'"
        self.wait_for(self.CHAT_BOX)
        self.wait_for(self.PLAYING_BUTTON)

    def _verify_streamer_profile_page(self):
        """Verifies elements specific to the streamer's profile page."""
        self.wait_for(self.STREAMER_NAME)
        self.wait_for(self.FOLLOWERS)
        self.wait_for(self.HOME_TAB)
        self.wait_for(self.ABOUT_TAB)
        self.wait_for(self.SCHEDULE_TAB)
        self.wait_for(self.VIDEOS_TAB)
        self.wait_for(self.CLIPS_TAB)
        self.wait_for(self.HOME_VIDEO)
    
