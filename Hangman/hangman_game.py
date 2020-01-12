from getWord import get_word
import constants
from table_highscores import RecordTable, PlayerResult


class HangMan:

    def __init__(self, record_table: RecordTable):
        self.used_symbols = []
        self.result_points = constants.RESULTS_POINTS
        self.count_possible_mistakes = constants.MAXIMUM_NUMBER_MISTAKES
        self.number_consecutive_valid_letters = constants.NUMBER_CONSECUTIVE_GUESSED_LETTERS
        self.bonus_points = constants.BONUS
        self.number_consecutive_invalid_letters = constants.NUMBER_CONSECUTIVE_ERRORS
        self.penalty_points = constants.SURCHARGE
        self.intermediate_points = constants.NUMBER_INTERMEDIATE_POINTS

        self.record_table = record_table

    # функция определения условий продолжения игры
    def game_continuation_conditions(self):
        return self.count_possible_mistakes > 0 and '*' in self.mask_word

    # функция определения условий для подсчета количества верно подряд отгаданных букв
    def is_determining_number_correctly_guessed_letter(self):
        self.number_consecutive_invalid_letters = 0
        self.number_consecutive_valid_letters += 1

    # функция определения условий для начисления бонусных баллов
    def conditions_receiving_penalty_points(self):
        return self.number_consecutive_valid_letters % 3 == 0 and self.number_consecutive_valid_letters > 0

    # функция определения условий для подсчета количества неверно подряд отгаданных букв
    def is_determining_number_incorrectly_guessed_letter(self):
        self.count_possible_mistakes -= 1
        self.number_consecutive_valid_letters = 0
        self.number_consecutive_invalid_letters += 1
        self.intermediate_points -= 2

    # функция определения условий для начисления штрафных баллов
    def conditions_receiving_penalty_points(self):
        return self.number_consecutive_invalid_letters % 3 == 0 and self.number_consecutive_invalid_letters > 0

    # функция получения итогового результата игры
    def get_results(self):
        if self.count_possible_mistakes == 0:
            self.result_points = int((-50 + self.intermediate_points + self.bonus_points + self.penalty_points) *
                                     len(self.hidden_word) / 6)

            return 'Вы проиграли! Загаданное слово: ' + self.hidden_word + '! Количество очков ' \
                   + str(self.result_points)

        else:
            self.result_points = int((50 + self.intermediate_points + self.bonus_points + self.penalty_points) *
                                     (6 / len(self.hidden_word)))
            return 'Вы выиграли! Вы отгадали слово: ' + self.hidden_word + '! Количество очков ' \
                   + str(self.result_points)

    def process_multiple_letters(self):
        self.is_determining_number_incorrectly_guessed_letter()
        print('Нельзя вводить несколько букв сразу!')
        print('Осталось ' + str(self.count_possible_mistakes) + ' раз ошибиться')

    def process_wrong_letter(self):
        self.is_determining_number_incorrectly_guessed_letter()
        print('Нет такой буквы!')
        print('Осталось ' + str(self.count_possible_mistakes) + ' раз ошибиться')
        print()

    def process_repeatable_letter(self):
        self.is_determining_number_incorrectly_guessed_letter()
        print('Вы уже вводили эту букву!')
        print('Осталось ' + str(self.count_possible_mistakes) + ' раз ошибиться')
        print()

    def process_empty_input(self):
        print('Вы ничего не ввели! Введите заново букву!')
        print()

    def process_found_letter(self, count_possible_symbol_in_hidden_word, possible_symbol):
        print('Есть такая буква!')
        print()
        key = -1

        for i in range(count_possible_symbol_in_hidden_word):
            index_guessed_letter = self.hidden_word.find(possible_symbol, 1 + key)
            self.mask_word[index_guessed_letter] = self.hidden_word[index_guessed_letter]
            key = index_guessed_letter

    # функция начала игры "Виселица"
    def start_game(self, hidden_word: str) -> str:
        self.player_name = input('Введите ваше имя: ')
        self.hidden_word = hidden_word
        self.mask_word = list('*' * len(hidden_word))

        while self.game_continuation_conditions():
            print(''.join(self.mask_word))

            possible_symbol = input('Введите букву слова:')
            count_possible_symbol_in_hidden_word = hidden_word.count(possible_symbol)

            # если пользователь ввел больше одной буквы
            if len(possible_symbol) > 1:
                self.process_multiple_letters()

            # если буква не угадана
            elif count_possible_symbol_in_hidden_word == 0:
                self.process_wrong_letter()

            # если пользователь ввел ту букву, которую уже вводил
            elif possible_symbol in self.used_symbols:
                self.process_repeatable_letter()

            # если пользователь не ввел букву
            elif len(possible_symbol) == 0:
                self.process_empty_input()

            else:
                self.process_found_letter(count_possible_symbol_in_hidden_word, possible_symbol)
                self.is_determining_number_correctly_guessed_letter()

                self.intermediate_points += 2 * count_possible_symbol_in_hidden_word

                if self.conditions_receiving_penalty_points():
                    self.bonus_points += 50 * self.number_consecutive_valid_letters

            self.used_symbols.append(possible_symbol)

            if self.conditions_receiving_penalty_points():
                self.penalty_points -= 40 * self.number_consecutive_invalid_letters // 3

        results = self.get_results()
        self.record_table.add_record(PlayerResult(
            name_player=self.player_name,
            count_points=self.result_points,
            count_mistakes=constants.MAXIMUM_NUMBER_MISTAKES - self.count_possible_mistakes
        ))

        return results


def game_mode_definition(flag):
    return flag == 'yes'


if __name__ == '__main__':

    game_mode = True
    record_table = RecordTable('db.json')

    while game_mode:
        game = HangMan(record_table)
        print(game.start_game(get_word()))
        print()
        print('Хотите ли вы еще сыграть в игру? (yes/no)')
        participant_decision = input()
        game_mode = game_mode_definition(participant_decision)
