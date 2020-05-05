#todo add logging
from libs.lib_screenshots.collect_screenshot import ScreenCollector
class ScreenAnalyzer(ScreenCollector):

    def __init__(self, config_selenium, config_analyser):
        super(ScreenAnalyzer, self).__init__(config_selenium)
        self.config_analyser = config_analyser


    def get_pixels_count(self, value):
        pixel_counter = 0
        for pixel in self.screen.getdata():
            pixel_counter += 1 if pixel[:3] == value else 0
        return pixel_counter

    def get_image_pixels(self, label, time):
        all_data =[]
        for elem in self.config_analyser['PIX_COLORS']:
            data = {
                'label': label,
                'timestamp' : time
            }
            data['color'] = elem['color']
            data['pix_values'] = str(elem['values'])
            data['count'] = self.get_pixels_count(elem['values'])
            all_data.append(data)

        return all_data