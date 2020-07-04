import pandas as pd
import statistics
import json
import matplotlib.pyplot as plt
import matplotlib as mpl
from collections import OrderedDict

class GetStatisticData:
    def __init__(self, file_name):
        self.file_name = file_name
        self.data = pd.read_csv(self.file_name)

    def determine_difference_price(self):
        all_prices = self.data['Цена']
        median_price = statistics.median(all_prices)
        average_price = int(statistics.mean(all_prices))
        mode_price = statistics.mode(all_prices)
        self.data['Разница цены в ₽ относительно медианной цены'] = self.data['Цена'] - median_price
        self.data['Разница цены в ₽ относительно средней цены'] = self.data['Цена'] - average_price
        self.data['Разница цены в ₽ относительно моды'] = self.data['Цена'] - mode_price
        self.data.to_csv(self.file_name)

    def determination_completeness_data_parsing(self):
        count_ads = len(self.data)

        count_correctly_recognized_phone_numbers, count_correctly_parsed_addresses, count_correctly_parsed_districts = 0, 0, 0

        for number_phone in self.data['Номер телефона']:
            if len(str(int(number_phone))) == 11:
                count_correctly_recognized_phone_numbers += 1
        coeff_correct_phone_number_recognition = count_correctly_recognized_phone_numbers / count_ads

        for address in self.data['Адрес']:
            if any(map(str.isdigit, address)) is True:
                count_correctly_parsed_addresses += 1
        coeff_correct_parsed_addresses = count_correctly_parsed_addresses / count_ads

        for district in self.data['Район']:
            if district != '':
                count_correctly_parsed_districts += 1
        coeff_correct_parsed_districts = count_correctly_parsed_districts / count_ads

        result_parsing = {
            'Количество объявлений': count_ads,
            'Номер телефона': 'Корректность ' + str(int(coeff_correct_phone_number_recognition * 100)) + '%',
            'Адрес': 'Корректность ' + str(int(coeff_correct_parsed_addresses * 100)) + '%',
            'Район': 'Корректность ' + str(int(coeff_correct_parsed_districts * 100)) + '%'
        }

        with open("ParsingResultReport.json", "w") as file:
            file.write(json.dumps(result_parsing, ensure_ascii=False))
            file.close()

        return result_parsing

    def draw_pie_chart_district_frequency(self):
        list_districts = sorted(self.data['Район'])

        frequency_occurrence_area = dict()
        for district in list_districts:
            if district not in frequency_occurrence_area:
                frequency_occurrence_area[district] = 0

                frequency_occurrence_area[district] += 1

        data_names = sorted(set(list_districts))

        dpi = 80
        fig = plt.figure(dpi=dpi, figsize=(1000 / dpi, 600 / dpi))
        mpl.rcParams.update({'font.size': 11})
        plt.title('Frequency of districts (%)')

        plt.pie(
            list(OrderedDict(frequency_occurrence_area).values()),
            autopct='%1.1f%%',
            shadow=True,
            radius=1.1,
            wedgeprops={'lw': 1, 'ls': '--', 'edgecolor': "k"},
            explode=[0.15] + [0 for _ in range(len(data_names) - 1)])
        plt.legend(
            bbox_to_anchor=(-0.16, 0.45, 0.25, 0.25),
            loc='best',
            labels=data_names)

        fig.savefig('pie.png')
