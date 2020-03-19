from PartOfSpeach import Word, Noun, Pronoun, Verb, Punctuation


class PosDetector(object):

    @staticmethod
    def detect_pos(token) -> Word:
        '''определение части речи'''
        tag = token['tag'][0]

        if tag == 'N':
            return Noun(token)
        elif tag == 'E':
            return Pronoun(token)
        elif tag == 'V':
            return Verb(token)
        elif tag == 'F':
            return Punctuation(token)
        else:
            return Word(token)


class WordUtils(object):
    @staticmethod
    def get_weight_of_word(word: Word):
        '''Определение веса, с которым данное может быть подлежащим'''
        if isinstance(word, Noun):
            if word.is_proper():
                return 3
            elif word.is_nominative():
                return 2
            else:
                return 0
        elif WordUtils.is_subject_based_pronoun(word):
            return 1
        return 0

    @staticmethod
    def is_subject_based_pronoun(word: Word) -> bool:
        return isinstance(word, Pronoun) and word.noun_based

    @staticmethod
    def is_proper_noun(word: Word) -> bool:
        return isinstance(word, Noun) and word.is_proper()

    @staticmethod
    def is_nominative_noun(word: Word) -> bool:
        return isinstance(word, Noun) and word.is_nominative()