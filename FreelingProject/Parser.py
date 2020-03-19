from MorphologyDetails import Gender, Number, Case


class Parser(object):
    @staticmethod
    def parse_gender(letter) -> Gender:
        if letter in ['M', 'F', 'N']:
            return Gender(letter)
        else:
            return Gender.Empty

    @staticmethod
    def parse_number(letter) -> Number:
        if letter in ['S', 'P']:
            return Number(letter)
        else:
            return Number.Empty

    @staticmethod
    def parse_case(letter) -> Case:
        if letter in ['N', 'G', 'D', 'F', 'C', 'O']:
            return Case(letter)
        else:
            return Case.Empty