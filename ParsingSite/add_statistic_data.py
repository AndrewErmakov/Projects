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
        pass


