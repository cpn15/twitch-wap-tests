import os
from dotenv import load_dotenv

load_dotenv()

class Data:

    DEVICE_NAME = os.environ["DEVICE_NAME"]
    TWITCH_URL = os.environ["TWITCH_URL"]
    LIVE_GAME = os.environ["LIVE_GAME"]
