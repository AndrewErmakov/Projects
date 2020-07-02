import argparse
import csv
import datetime

import requests
from bs4 import BeautifulSoup
from pprint import pprint

from secrets import URL, DOMAIN, headline, count_rooms
from parser_tel_number import NumberPhone
from parser_district_city import DefinitionGeoLocation, AlternativeWayDefinitionGeoLocation
from sent_file_result_parsing import EmailResults
from add_statistic_data import GetStatisticData

headlines = {
    'купить': 'prodam',
    'снять': 'sdam'
}


class Writer:
    def __init__(self, file_name):
        self.file_name = f'{file_name}.csv'
        self.file = open(self.file_name, 'w')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['Краткая основная информация',
                              'Цена',
                              'Адрес',
                              'Ссылка на объявление',
                              'Номер телефона',
                              'Район'])

    def write(self, data):
        self.writer.writerow((data['title'],
                              data['price'],
                              data['address'],
                              data['url'],
                              data['phone'],
                              data['district']))

    def __del__(self):
        self.file.close()


def get_html(url):
    r = requests.get(url)
    return r.text


def get_total_pages(html):
    """Функция определения количества страниц"""
    soup = BeautifulSoup(html, 'html.parser')
    pages = soup.find('div', class_='pagination-root-2oCjZ').find_all('span', class_='pagination-item-1WyVp')
    count_total_pages = pages[-2].get_text()
    return count_total_pages


def get_page_data(html, file_name):
    """Функция получения данных страницы"""
    soup = BeautifulSoup(html, 'html.parser')

    ads = soup.find('div', class_='snippet-list js-catalog_serp').find_all('div',
                                                                           class_='description item_table-description')

    writer = Writer(file_name)
    geo_location = DefinitionGeoLocation()
    for ad in ads:

        number_phone_recognition = NumberPhone()  # Определение экземпляра класса определения номера телефона
        title = ad.find('div', class_='snippet-title-row').find('h3').text.strip().replace(',', '')
        url = DOMAIN + ad.find('div', class_='snippet-title-row').find('h3').find('a').get('href')
        try:
            number_phone = int(number_phone_recognition.main(url))
        except:
            number_phone = ''
        price = ad.find('div', class_='snippet-price-row').find('span', class_='snippet-price').text.strip().replace('в месяц', '').strip().replace('₽', '').strip().replace(' ', '')
        address = ad.find('div', class_='item-address').find('span', class_='item-address__string').text.strip().replace('ул.', '').replace(',', '').strip().replace('  ', ' ')

        try:
            district = geo_location.get_name_district(address).strip()

        except Exception as e:
            alternative_way_get_district = AlternativeWayDefinitionGeoLocation()
            district = alternative_way_get_district.alternative_way_get_name_district(address)

        data = {
            'title': title,
            'price': price,
            'address': address,
            'url': url,
            'phone': number_phone,
            'district': district
        }

        writer.write(data)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--count_rooms", type=int,
                        help="display a number of rooms in flat of your dream",
                        default=1,
                        choices=range(1, 6))

    parser.add_argument('--search_purpose', type=str,
                        help="display a type of ad about flat",
                        default='снять',
                        choices=['снять', 'купить'])

    parser.add_argument('--file_name', type=str,
                        help='name of the file to save the parsing result to (in the format csv)',
                        default='Results' + datetime.datetime.today().strftime("%Y%m%d"))

    parser.add_argument('--solution_for_send_file', action='store_true',
							help='Do you want to send the result of parsing to mail?')

    arguments = parser.parse_args()

    count_rooms = str(arguments.count_rooms)
    file_name = arguments.file_name
    headline = headlines[arguments.search_purpose]
    solution_for_send_file = arguments.solution_for_send_file

    get_page_data(get_html(URL), file_name)

    get_statistic_data = GetStatisticData(f'{file_name}.csv')
    get_statistic_data.determine_difference_price()
    pprint(get_statistic_data.determination_completeness_data_parsing())

    if bool(solution_for_send_file) is True:
        send_results = EmailResults()
        send_results.send_file(f'{file_name}.csv')
