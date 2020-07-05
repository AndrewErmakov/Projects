import argparse
import csv
import datetime

import requests
from bs4 import BeautifulSoup

from secrets import URL, DOMAIN, headline, count_rooms, optional_info
from parser_tel_number import NumberPhone
from parser_district_city import DefinitionGeoLocation, AlternativeWayDefinitionGeoLocation
from sent_file_result_parsing import EmailResults
from add_statistic_data import GetStatisticData

headlines = {
    'купить': ['prodam', '', '?'],
    'снять': ['sdam', '/na_dlitelnyy_srok', '&']
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
    return int(count_total_pages)

def get_link_with_all_ads(html):
    soup = BeautifulSoup(html, 'html.parser')
    current_link_with_ads = soup.find('div', {'class': 'pagination-pages clearfix'}).find('a', {'class': 'pagination-page'}).get('href')
    return DOMAIN + current_link_with_ads


def get_page_data(html, writer):
    """Функция получения данных страницы"""
    soup = BeautifulSoup(html, 'html.parser')

    ads = soup.find('div', class_='snippet-list js-catalog_serp').find_all('div',
                                                                           class_='description item_table-description')

    geo_location = DefinitionGeoLocation()
    for ad in ads:

        number_phone_recognition = NumberPhone()  # Определение экземпляра класса определения номера телефона
        title = ad.find('div', class_='snippet-title-row').find('h3').text.strip().replace(',', '')
        url = DOMAIN + ad.find('div', class_='snippet-title-row').find('h3').find('a').get('href')
        try:
            number_phone = int(number_phone_recognition.main(url))
        except Exception as e:
            number_phone = 'Not found'
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

    headline = headlines[arguments.search_purpose][0]
    optional_info = headlines[arguments.search_purpose][1]
    symbol_page = headlines[arguments.search_purpose][2]

    solution_for_send_file = arguments.solution_for_send_file


    total_pages = get_total_pages(get_html(URL))

    full_url = get_link_with_all_ads(get_html(URL))

    writer = Writer(file_name)

    for num_page in range(1, total_pages + 1):
        get_page_data(get_html(full_url + f'{symbol_page}p={num_page}'), writer)
        print(f'Закончена страница {num_page}')

    get_statistic_data = GetStatisticData(f'{file_name}.csv')
    get_statistic_data.determine_difference_price()
    get_statistic_data.draw_pie_chart_district_frequency()


    if bool(solution_for_send_file) is True:
        send_results = EmailResults()
        send_results.send_file(f'{file_name}.csv')
