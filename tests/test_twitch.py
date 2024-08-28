from config.Data import Data
from pages.twitch_page import TwitchPage

def test_twitch_streamer(driver):

    driver.get(Data.TWITCH_URL)
    TwitchPage(driver)\
        .search_for_a_game(Data.LIVE_GAME)\
        .wait_for_search_results_page()\
        .scroll_down(2)\
        .select_random_streamer_from_channels()\
        .handle_content_warning()\
        .wait_for_load_and_take_screenshot()
    