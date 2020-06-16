import csv

import requests
from bs4 import BeautifulSoup

from secrets import URL, DOMAIN
from parser_tel_number import NumberPhone


class Writer:
    def __init__(self):
        self.file_name = 'data.csv'
        self.file = open(self.file_name, 'w')
        self.writer = csv.writer(self.file)
        self.writer.writerow(['Краткая основная информация',
                              'Цена',
                              'Адрес',
                              'Ссылка на объявление',
                              'Номер телефона'])

    def write(self, data):
        self.writer.writerow((data['title'],
                              data['price'],
                              data['address'],
                              data['url'],
                              data['phone']))

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

        data = {
            'title': title,
            'price': price,
            'address': address,
            'url': url,
            'phone': number_phone
        }

        writer.write(data)


if __name__ == '__main__':
    get_page_data(get_html(URL))
