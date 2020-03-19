from enum import Enum


class Case(Enum):
    Nominative = 'N'
    Genitive = 'G'
    Dative = 'D'
    Accusative = 'F'
    Instrumental = 'C'
    Prepositional = 'O'
    Empty = None


class Gender(Enum):
    Masculine = 'M'
    Feminine = 'F'
    Neuter = 'N'
    Empty = None


class Number(Enum):
    Singular = 'S'
    Plural = 'P'
    Empty = None


class PartSentence(Enum):
    Subject = 'S'
    Predicate = 'P'
    Empty = None