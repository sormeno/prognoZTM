#todo add logging

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from PIL import Image
from io import BytesIO
import base64

class ScreenCollector:

    def __init__(self, config):
        self.driver = webdriver.Chrome(options=self.options(config), executable_path="C:\\chromedriver\\chromedriver.exe")


    def options(self, config):
        options = Options()
        for elem in config:
            options.add_argument(elem)
        return options


    def get_screen(self, url):
        self.driver.get(url)
        screen = self.driver.get_screenshot_as_base64()
        return Image.open(BytesIO(base64.b64decode(screen)))
