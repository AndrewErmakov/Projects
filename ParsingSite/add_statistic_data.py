import pandas as pd
import statistics

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
            if str(len(number_phone)) == 11:
                count_correctly_recognized_phone_numbers += 1
        coeff_correct_phone_number_recognition = count_correctly_recognized_phone_numbers / count_ads

        for address in self.data['Адрес']:
            if any(map(str.isdigit, 'qwe1')) is True:
                count_correctly_parsed_addresses += 1
        coeff_correct_parsed_addresses = count_correctly_parsed_addresses / count_ads

        for district in self.data['Район']:
            if district != '':
                count_correctly_parsed_districts += 1
        coeff_correct_parsed_districts = count_correctly_parsed_districts / count_ads

        result_parsing = {
            'Номер телефона': 'Корректность' + str(int(coeff_correct_phone_number_recognition * 100)) + '%',
            'Адрес': 'Корректность' + str(int(coeff_correct_parsed_addresses * 100)) + '%',
            'Район': 'Корректность' + str(int(coeff_correct_parsed_districts * 100)) + '%'
        }

        with open("ParsingResultReport.json", "w") as file:
            json.dumps(result_parsing, file)
            file.close()

        return result_parsing
