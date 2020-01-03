import os
import random


def get_word() -> str:
    """
    Функция генерирует слово, которое нужно отгадать пользователю.
    В качестве подсказки выводится предметная область этого слова.
    """

    list_words = [['металлы', 'олово', 'серебро', 'сталь', 'свинец', 'золото', 'бронза', 'алюминий', 'медь'],
                  ['транспорт', 'автомобиль', 'мотоцикл', 'автобус', 'самолет', 'вертолет', 'троллейбус', 'поезд',
                   'грузовик'],
                  ['животные', 'собака', 'енот', 'выдра', 'крыса', 'волк', 'медведь', 'лиса', 'заяц']
                  ]
    number_theme = random.randint(0, len(list_words) - 1)
    print('Тема: ' + list_words[number_theme][0])
    word = random.choice(list_words[number_theme][1:])
    return word


def start_game(hidden_word: str) -> str:
    mask_word = list('*' * len(hidden_word))

    count_possible_mistakes = 10
    used_symbols = []

    while count_possible_mistakes > 0 and '*' in mask_word:
        print(''.join(mask_word))

        print('Введите букву слова:')
        possible_symbol = input()

        count_possible_symbol_in_hidden_word = hidden_word.count(possible_symbol)

        if len(possible_symbol) > 1:
            count_possible_mistakes -= 1
            print('Нельзя вводить несколько букв сразу!')
            print('Осталось ' + str(count_possible_mistakes) + ' раз ошибиться')

        elif count_possible_symbol_in_hidden_word == 0:
            count_possible_mistakes -= 1
            print('Нет такой буквы!')
            print('Осталось ' + str(count_possible_mistakes) + ' раз ошибиться')

        # если пользователь ввел ту букву, которую уже вводил
        elif possible_symbol in used_symbols:
            count_possible_mistakes -= 1
            print('Вы уже вводили эту букву!')
            print('Осталось ' + str(count_possible_mistakes) + ' раз ошибиться')

        # если пользователь не ввел букву
        elif len(possible_symbol) == 0:
            print('Вы ничего не ввели! Введите заново букву!')

        else:
            print('Есть такая буква!')
            key = -1

            for i in range(count_possible_symbol_in_hidden_word):
                index_guessed_letter = hidden_word.find(possible_symbol, 1 + key)
                mask_word[index_guessed_letter] = hidden_word[index_guessed_letter]
                key = index_guessed_letter

        used_symbols.append(possible_symbol)

    if count_possible_mistakes == 0:
        return 'Вы проиграли! Загаданное слово: ' + hidden_word

    else:
        return 'Вы выиграли! Вы отгадали слово: ' + hidden_word


def game_mode_definition(flag):
    if flag == 'yes':
        return True

    elif flag == 'no':
        return False


# def clear_screen():
#     try:
#         os.system('clear')
#
#     except:
#         os.system('cls')


game_mode = True
while game_mode:

    print(start_game(get_word()))
    print()
    print('Хотите ли вы еще сыграть в игру? (yes/no)')
    participant_decision = input()
    game_mode = game_mode_definition(participant_decision)
    # print('\n' * 25)
