import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from PIL import Image

from pytesseract import image_to_string


class NumberPhone:
    def __init__(self):
        self.options = Options()
        self.options.headless = True
        self.driver = webdriver.Firefox(options=self.options)

        os.makedirs('screenshots', exist_ok=True)

    def navigate(self, url):
        self.driver.get(url)

        time.sleep(15)
        button = self.driver.find_element(By.CLASS_NAME, 'js-item-phone-number')
        button.click()

        time.sleep(3)
        self.take_screenshot()

        # image_phone = self.driver.find_element(By.CLASS_NAME, 'item-phone-big-number').find_element(By.TAG_NAME, 'img').get_attribute('src')

        image_phone = self.driver.find_element_by_xpath(
            '//div[@class="item-phone-big-number js-item-phone-big-number"]/img')

        location = image_phone.location
        size = image_phone.size

        phone = self.phone_recognition(location, size)
        return phone

    def take_screenshot(self):
        self.driver.save_screenshot('screenshots/screenshot.png')

    def crop(self, location, size):
        image = Image.open('screenshots/screenshot.png')
        x = location['x']
        y = location['y']
        width = size['width']
        height = size['height']

        image.crop((x, y, x + width, y + height)).save('screenshots/screenshot.png')

    def phone_recognition(self, location, size):
        self.crop(location, size)
        image = Image.open('screenshots/screenshot.png')
        number_phone = image_to_string(image).replace(' ', '').replace('-', '')
        return number_phone



