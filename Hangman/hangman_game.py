from getWord import get_word
from constants import MAXIMUM_NUMBER_MISTAKES


class HangMan:

    def game_continuation_conditions(self):
        return self.count_possible_mistakes > 0 and '*' in self.mask_word

    # def letters_mismatch(self, possible_symbol, count_possible_symbol_in_hidden_word):

    def get_results(self):
        if self.count_possible_mistakes == 0:
            return 'Вы проиграли! Загаданное слово: ' + self.hidden_word

        else:
            return 'Вы выиграли! Вы отгадали слово: ' + self.hidden_word

    def process_multiple_letters(self):
        self.count_possible_mistakes -= 1
        print('Нельзя вводить несколько букв сразу!')
        print('Осталось ' + str(self.count_possible_mistakes) + ' раз ошибиться')

    def process_wrong_letter(self):
        self.count_possible_mistakes -= 1
        print('Нет такой буквы!')
        print('Осталось ' + str(self.count_possible_mistakes) + ' раз ошибиться')
        print()

    def process_repeatable_letter(self):
        self.count_possible_mistakes -= 1
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

    def start_game(self, hidden_word: str) -> str:

        self.hidden_word = hidden_word
        self.used_symbols = []
        self.count_possible_mistakes = MAXIMUM_NUMBER_MISTAKES
        self.mask_word = list('*' * len(hidden_word))

        while self.game_continuation_conditions():
            print(''.join(self.mask_word))

            print('Введите букву слова:')
            possible_symbol = input()

            count_possible_symbol_in_hidden_word = hidden_word.count(possible_symbol)

            # если пользователь ввел больше одной буквы
            if len(possible_symbol) > 1:
                self.process_multiple_letters()

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

            self.used_symbols.append(possible_symbol)

        return self.get_results()


class RecordTable:
    pass


def game_mode_definition(flag):
    return flag == 'yes'


if __name__ == '__main__':

    game_mode = True

    while game_mode:
        game = HangMan()
        print(game.start_game(get_word()))
        print()
        print('Хотите ли вы еще сыграть в игру? (yes/no)')
        participant_decision = input()
        game_mode = game_mode_definition(participant_decision)
        # print('\n' * 25)

