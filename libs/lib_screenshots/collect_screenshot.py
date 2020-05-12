import logging
logger = logging.getLogger('prognoZTM.collect_screenshot')

from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from PIL import Image
from io import BytesIO
import base64

class ScreenCollector:

    def __init__(self, config):
        self.driver = webdriver.Chrome(options=self.options(config.get('config')),
                                       executable_path=config.get('browser_driver'))


    def options(self, config):
        options = Options()
        logger.info(f'Setting selenium options.')
        for elem in config:
            options.add_argument(elem)
            logger.info(f'Options {elem} added')
        return options


    def get_screen(self, url):
        logger.debug(f'Taking screenshot with url: {url}')
        self.driver.get(url)
        logger.debug(f'Screenshot taken')
        logger.debug(f'Converting screenshot to PIL image format')
        screen = self.driver.get_screenshot_as_base64()
        self.screen = Image.open(BytesIO(base64.b64decode(screen)))
        logger.debug(f'Screenshot converted.')
        return self
