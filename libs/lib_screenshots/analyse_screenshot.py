import logging
logger = logging.getLogger('prognoZTM.analyse_screenshot')

from libs.lib_screenshots.collect_screenshot import ScreenCollector
class ScreenAnalyzer(ScreenCollector):

    def __init__(self, config_selenium, config_analyser):
        super(ScreenAnalyzer, self).__init__(config_selenium)
        self.config_analyser = config_analyser
        logger.info(f'ScreenAnalyzer initiated with following config:\n{self.config_analyser}')


    def get_pixels_count(self, value):
        pixel_counter = 0
        for pixel in self.screen.getdata():
            pixel_counter += 1 if pixel[:3] == value else 0
        logger.debug(f'{pixel_counter} pixels found')
        return pixel_counter

    def get_image_pixels(self, label, time):
        pixels_count =[]
        logger.debug(f'Iterrating {label} image over defined pixel colours with timestamp: {time}')
        for elem in self.config_analyser['PIX_COLORS']:
            data = {
                'label': label,
                'timestamp': time
            }
            data['color'] = elem.get('color')
            data['pix_values'] = str(elem.get('values'))
            logger.debug(f'Counting {elem.get("color")} {elem.get("values")} pixels')
            data['count'] = self.get_pixels_count(elem.get('values'))
            pixels_count.append(data)
            logger.debug(f'Pixels data appended with: \n{data}')


        return pixels_count