import pandas as pd
import statistics

class PricingDetermination:
    def __init__(self, file_name):
        self.file_name = file_name

    def determine_difference_price(self):
        data = pd.read_csv(self.file_name)
        all_prices = data['Цена']
        median_price = statistics.median(all_prices)
        average_price = int(statistics.mean(all_prices))
        mode_price = statistics.mode(all_prices)
        data['Разница цены в ₽ относительно медианной цены'] = data['Цена'] - median_price
        data['Разница цены в ₽ относительно средней цены'] = data['Цена'] - average_price
        data['Разница цены в ₽ относительно моды'] = data['Цена'] - mode_price
        data.to_csv(self.file_name)
