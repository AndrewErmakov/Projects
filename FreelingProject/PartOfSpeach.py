from typing import List

from MorphologyDetails import PartSentence, Gender, Number, Case
from Parser import Parser


class Word(object):
    tagset: str
    lemma: str
    word: str
    links: List[int]
    part_sentence: PartSentence
    frequency: int

    def __init__(self, token):
        self.tagset = token['tag']
        self.lemma = token['lemma']
        self.word = token['form']
        self.part_sentence = PartSentence.Empty
        self.links = []
        self.frequency = 0


class Noun(Word):
    gender: Gender
    number: Number
    case: Case
    common: bool

    def __init__(self, token):
        super().__init__(token)
        self.common = self.tagset[1] == 'C'

        if self.common:
            self.gender = Parser.parse_gender(self.tagset[4])
            self.case = Parser.parse_case(self.tagset[2])
            self.number = Parser.parse_number(self.tagset[3])
        else:
            self.gender = Gender.Empty
            self.case = Case.Empty
            self.number = Number.Empty

    def is_proper(self):
        return not self.common

    def is_nominative(self):
        return self.common and self.case == Case.Nominative


class Pronoun(Word):
    number: Number
    noun_based: bool

    def __init__(self, token):
        super().__init__(token)

        self.number = Parser.parse_number(self.tagset[2])
        self.noun_based = Parser.parse_case(self.tagset[1]) == Case.Empty or Parser.parse_case(self.tagset[1]) == Case.Nominative


class Verb(Word):
    number: Number
    gender: Gender
    infinitive: bool

    def __init__(self, token):
        super().__init__(token)
        self.number = Parser.parse_number(self.tagset[2])
        self.gender = Parser.parse_gender(self.tagset[3])
        self.infinitive = self.tagset[1] == 'I' and self.number == Number.Empty


class Punctuation(Word):
    is_end: bool

    def __init__(self, token):
        super().__init__(token)


        self.is_end = self.tagset[1] in ['a', 'i', 't']