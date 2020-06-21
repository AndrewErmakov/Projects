import json

import requests
from secrets import API_KEY, BASE_URL, DESIRED_CITY


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


