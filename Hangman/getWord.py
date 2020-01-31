import random
import json
from pprint import pprint


# def get_word() -> str:
#     """
#     Функция генерирует слово, которое нужно отгадать пользователю.
#     В качестве подсказки выводится предметная область этого слова.
#     """
#
#     dict_words = {'металлы': ['олово', 'серебро', 'сталь', 'свинец', 'золото', 'бронза', 'алюминий', 'медь'],
#                   'транспорт': ['автомобиль', 'мотоцикл', 'автобус', 'самолет', 'вертолет', 'троллейбус', 'поезд',
#                                 'грузовик'],
#                   'животные': ['собака', 'енот', 'выдра', 'крыса', 'волк', 'медведь', 'лиса', 'заяц'],
#                   'спорт': ['футбол', 'хоккей', 'бейсбол', 'бокс', 'самбо', 'плавание', 'регби', 'баскетбол'],
#                   'бизнес': ['реноме', 'маклер', 'экспансия', 'номинал', 'вето', 'баланс', 'пивот', 'коммитмент'],
#                   'математика': ['аксиома', 'константа', 'логарифм', 'экспонента', 'процент', 'дробь', 'дискриминант',
#                                  'конус'],
#                   'продукты питания': ['молоко', 'масло', 'хлеб', 'сыр', 'рис', 'макароны', 'кефир', 'рыба', 'мясо'],
#                   'рыбы': ['карась', 'кета', 'анчоус', 'карп', 'окунь', 'пелядь', 'палтус', 'сайра', 'скумбрия', 'скат'],
#                   'марки автомобилей': ['вольво', 'ауди', 'лада', 'инфинити', 'форд', 'киа', 'мазда', 'шкода', 'рено'],
#                   'одежда': ['футболка', 'рубашка', 'шорты', 'брюки', 'джинсы', 'пиджак', 'майка', 'куртка'],
#                   'канцтовары': ['ручка', 'карандаш', 'тетрадь', 'ластик', 'блокнот', 'дырокол', 'калькулятор', 'доска'],
#                   'посуда': ['вилка', 'сервиз', 'нож', 'тарелка', 'казан', 'кастрюля', 'сковорода', 'ложка']
#                   }
#
# title_theme = random.choice(list(dict_words.keys()))
# print('Тема: ' + title_theme)
# word = random.choice(dict_words[title_theme])
# return word
#

class Vocabulary:
    def __init__(self):
        self.vocabulary_db_file = 'vocabulary.json'

    def read_dict_words(self):
        with open(self.vocabulary_db_file, 'r') as file:
            self.data = json.loads(file.read())
            return self.data

    def get_word(self):
        self.title_theme = random.choice(list(self.read_dict_words().keys()))
        print('Тема: ' + self.title_theme)
        self.word = random.choice(self.read_dict_words()[self.title_theme])
        return self.word

    def update_dict_words(self, new_data):
        with open(self.vocabulary_db_file, 'w') as file:
            file.write(json.dumps(new_data))

    def add_new_word(self):
        current_words = self.read_dict_words()
        print('ДО')
        pprint(current_words)
        subject_new_word = input("Введите тематику нового слова:")
        added_words = input("Введите добавляемое слово(а):").split()
        if subject_new_word not in current_words:
            current_words[subject_new_word] = []
            for new_word in added_words:
                if new_word not in current_words[subject_new_word]:
                    current_words[subject_new_word].append(new_word)

        else:
            for new_word in added_words:
                if new_word not in current_words[subject_new_word]:
                    current_words[subject_new_word].append(new_word)

        self.update_dict_words(current_words)
        print('ПОСЛЕ')
        pprint(current_words)

# vocabulary = Vocabulary()
# dict_words = vocabulary.read_dict_words()
# print('ДО')
# pprint(dict_words)
# theme = input("Введите тему:")
# added_words = input("Введите добавляемое слово(а):").split()
# if theme not in dict_words:
#     dict_words[theme] = []
#     for word in added_words:
#         if word not in dict_words[theme]:
#             dict_words[theme].append(word)
#
# else:
#
#     for word in added_words:
#         if word not in dict_words[theme]:
#             dict_words[theme].append(word)
#
# # dict_words[theme].remove('альвадос')
# update_dict_words(dict_words)
#
# print('ПОСЛЕ')
# pprint(dict_words)
#
# title_theme = random.choice(list(dict_words.keys()))
# print('Тема: ' + title_theme)
#
# wrd = random.choice(dict_words[title_theme])
# print('Слово: ' + wrd)

