import base64
import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

from PIL import Image
from pytesseract import image_to_string


class NumberPhone:
    def __init__(self):
        self.options = Options()
        self.options.headless = True
        self.driver = webdriver.Firefox(options=self.options)
        os.makedirs('screenshots', exist_ok=True)
        self.counter_screenshots = 1

    def main(self, url):
        telephone_number_page = self.navigate_to_telephone_number_page(url)

        base64_string_link_image_number_phone = self.get_link_base64_image_number_phone(telephone_number_page)
        file_path = 'screenshots/screen' + str(self.counter_screenshots) + '.png'
        self.save_image_number_phone(base64_string_link_image_number_phone, file_path)

        number_phone = self.phone_recognition(file_path)
        return number_phone

    def navigate_to_telephone_number_page(self, url):
        self.driver.get(url)
        time.sleep(15)
        button = self.driver.find_element(By.CLASS_NAME, 'js-item-phone-number')
        button.click()
        time.sleep(3)
        telephone_number_page = self.driver.page_source
        self.driver.quit()
        return telephone_number_page

    def get_link_base64_image_number_phone(self, html_page):
        soup = BeautifulSoup(html_page, 'html.parser')
        try:
            link_image_number_phone = soup.find('div', class_='popup-content').find(
                'div', class_='item-popup-content js-item-phone-popup-content').find(
                'div', class_='item-phone-big-number js-item-phone-big-number').find('img').attrs['src']

        except AttributeError:
            link_image_number_phone = 'Not found'

        return link_image_number_phone

    def save_image_number_phone(self, base64_link, file_name):
        base64_link = base64_link.replace('data:image/png;base64,', '')
        img_data = base64.b64decode(base64_link)
        with open(file_name, 'wb') as file:
            file.write(img_data)
            file.close()

    def phone_recognition(self, image):
        image_number_phone = Image.open(image)
        number_phone = image_to_string(image_number_phone).replace(' ', '').replace('-', '')
        return number_phone


