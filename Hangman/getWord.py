import random


def get_word() -> str:
    """
    Функция генерирует слово, которое нужно отгадать пользователю.
    В качестве подсказки выводится предметная область этого слова.
    """

    list_words = [['металлы', 'олово', 'серебро', 'сталь', 'свинец', 'золото', 'бронза', 'алюминий', 'медь'],
                  ['транспорт', 'автомобиль', 'мотоцикл', 'автобус', 'самолет', 'вертолет', 'троллейбус', 'поезд',
                   'грузовик'],
                  ['животные', 'собака', 'енот', 'выдра', 'крыса', 'волк', 'медведь', 'лиса', 'заяц'],
                  ['спорт', 'футбол', 'хоккей', 'бейсбол', 'бокс', 'самбо', 'плавание', 'регби', 'баскетбол'],
                  ['бизнес', 'реноме', 'маклер', 'экспансия', 'номинал', 'вето', 'баланс', 'паблисити', 'фас']
                  ]
    number_theme = random.randint(0, len(list_words) - 1)
    print('Тема: ' + list_words[number_theme][0])
    word = random.choice(list_words[number_theme][1:])
    return word

