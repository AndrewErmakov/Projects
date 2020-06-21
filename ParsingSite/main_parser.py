import csv

import requests
from bs4 import BeautifulSoup

from secrets import URL, DOMAIN
from parser_tel_number import NumberPhone
from parser_district_city import DefinitionGeoLocation
from sent_file_result_parsing import EmailResults


class Writer:
    def __init__(self):
        self.file_name = 'data.csv'
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


def get_page_data(html):
    """Функция получения данных страницы"""
    soup = BeautifulSoup(html, 'html.parser')

    ads = soup.find('div', class_='snippet-list js-catalog_serp').find_all('div',
                                                                           class_='description item_table-description')

    writer = Writer()
    geo_location = DefinitionGeoLocation()
    for ad in ads:

        number_phone_recognition = NumberPhone()  # Определение экземпляра класса определения номера телефона
        title = ad.find('div', class_='snippet-title-row').find('h3').text.strip()
        url = DOMAIN + ad.find('div', class_='snippet-title-row').find('h3').find('a').get('href')
        try:
            number_phone = number_phone_recognition.main(url)
        except:
            number_phone = ''
        price = ad.find('div', class_='snippet-price-row').find('span', class_='snippet-price').text.strip()
        address = ad.find('div', class_='item-address').find('span', class_='item-address__string').text.strip()

        try:
            district = geo_location.get_name_district(address)
        except:
            district = ''

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
    get_page_data(get_html(URL))
    solution_for_send_file = input('Do you want to send the result of parsing to mail? (y/n)')

    if solution_for_send_file.lower()[0] in ['y', 'д']:
        send_results = EmailResults()
        send_results.send_file('data.csv')


