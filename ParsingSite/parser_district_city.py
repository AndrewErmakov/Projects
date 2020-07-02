import json
import time
import requests

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from secrets import API_KEY, BASE_URL, DESIRED_CITY, URL_ALTERNATIVE_SEARCH_DISTRICT


class DefinitionGeoLocation:
    def __init__(self):
        self.url = BASE_URL
        self.api_key = API_KEY
        self.desired_city = DESIRED_CITY

    def suggest(self, query):
        headers = {
            'Authorization': 'Token ' + self.api_key,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }

        data = {
            'query': query,
            "count": 20
        }
        response = requests.post(self.url, data=json.dumps(data), headers=headers)
        return response.json()

    def get_name_district(self, address):
        all_geo_info = self.suggest(self.desired_city + address)
        name_district = all_geo_info['suggestions'][0]['data']['city_district']
        return name_district

class AlternativeWayDefinitionGeoLocation:
    def __init__(self):
        self.options = Options()
        self.options.headless = True
        self.driver = webdriver.Firefox(options=self.options)
        self.desired_city = DESIRED_CITY

    def navigate_to_district(self, address):
        url = URL_ALTERNATIVE_SEARCH_DISTRICT
        self.driver.get(url)
        time.sleep(15)

        field_entering_address = self.driver.find_element(By.CLASS_NAME, 'form-control')
        field_entering_address.send_keys(address)
        time.sleep(15)

        district_definition_button = self.driver.find_element_by_id('getDistrictButton')
        district_definition_button.click()
        time.sleep(15)

        full_name_district = self.driver.find_element_by_id('result-element').find_element_by_tag_name('a').text
        field_entering_address.clear()
        self.driver.quit()

        return full_name_district

    def alternative_way_get_name_district(self, address):
        full_name_district = self.navigate_to_district(self.desired_city + address)
        district = full_name_district.split()[0]
        return district
