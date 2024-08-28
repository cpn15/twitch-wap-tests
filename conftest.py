import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from config.Data import Data

@pytest.fixture(scope="function")
def driver():
    """Fixture for the selenium WebDriver instance."""

    options = Options()
    options.add_experimental_option(\
        "mobileEmulation", {"deviceName": Data.DEVICE_NAME})
    driver = webdriver.Chrome(\
        service=Service(ChromeDriverManager().install()), options=options)
    
    driver.maximize_window()
    
    yield driver
    driver.quit()
    