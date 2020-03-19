import json
from collections.__init__ import defaultdict
from os import path
from subprocess import run, PIPE
from typing import List, Optional, Tuple

from MorphologyDetails import PartSentence, Gender
from PartOfSpeach import Word, Verb
from WordUtils import PosDetector, WordUtils


class KeyWordSearcher(object):
    def __init__(
            self,
            path_to_text_file,
            language='ru'
    ):
        self._path_to_text_file = path_to_text_file
        self._language = language

        self._sentences = None
        if not path.exists(self._path_to_text_file):
            print('No file in', self._path_to_text_file)
            raise FileNotFoundError

    def parse_text(self):
        '''

        Запускаем freeling, результат анализа текста записывается в формате json
        '''
        process = run([
                r'C:\freeling\freelingAll\freeling-bin\bin\analyzer.bat',
                '-f', f'{self._language}.cfg',
                '--mode', 'doc',
                '--flush',
                '--output', 'json'
            ],
            stdout=PIPE,
            input=open(self._path_to_text_file, 'rb').read(),
            stderr=PIPE
        )

        document = json.loads(process.stdout)

        self._sentences = document['paragraphs'][0]['sentences']


    def prepare_tokens(self):
        '''
        Определяет часть речи в каждом предложении
        '''
        self._sentences = [
            [
                PosDetector.detect_pos(token) for token in sentence['tokens'] if len(token) > 2
            ] for sentence in self._sentences
        ]

    def update_part_sentence(self, sentence: List[Word]) -> List[Word]:
        '''
        Определяет подлежащее и сказуемое в конкретном предложении
        '''
        word_weights = []

        for word in sentence:
            if isinstance(word, Verb):
                word.part_sentence = PartSentence.Predicate
            word_weight = WordUtils.get_weight_of_word(word)
            word_weights.append(word_weight)

        max_word_weight = max(word_weights)
        if max_word_weight == 0:
            return sentence

        result = []
        for word, word_weight in zip(sentence, word_weights):
            if word_weight == max_word_weight:
                word.part_sentence = PartSentence.Subject

            result.append(word)
        return result

    def define_document_part_sentence(
            self
    ):
        self._sentences = [
            self.update_part_sentence(sentence) for sentence in self._sentences
        ]


    def update_word_by_state(
            self,
            word: Word,
            state: Optional[Word]
    ) -> Tuple[Word, Optional[Word]]:
        if state is None or not WordUtils.is_subject_based_pronoun(word):
            return word, word
        if state.number == word.number or WordUtils.is_proper_noun(state):
            word.lemma = state.lemma
            return word, state
        return word, word

    def replace_lemmas_for_pronouns(self):
        state_word = None
        updated_sentences = []
        for sentence in self._sentences:
            updated_sentence = []
            for word in sentence:
                if word.part_sentence == PartSentence.Subject:
                    updated_word, state_word = self.update_word_by_state(word, state_word)
                    updated_sentence.append(updated_word)
                else:
                    updated_sentence.append(word)
            updated_sentences.append(updated_sentence)
        self._sentences = updated_sentences

    def calculate_frequencies(self):
        """Вычисляется частота вхождения каждого подлежащего"""
        frequencies = defaultdict(int)

        for sentence in self._sentences:
            for word in sentence:
                if word.part_sentence == PartSentence.Subject:
                    frequencies[word.lemma] += 1

        for sentence in self._sentences:
            for word in sentence:
                word.frequency = frequencies.get(word.lemma)


    def set_subject_object(self):
        '''Каждому подлежащему ставится одно или несколько сказуемых'''
        for sentence in self._sentences:
            subject_words = [word for word in sentence if word.part_sentence == PartSentence.Subject]
            predicate_words = [word for word in sentence if word.part_sentence == PartSentence.Predicate]

            for subject in subject_words:
                for predicate in predicate_words:
                    if self.is_base(subject, predicate):
                        subject.links.append(predicate)


    def is_base(self, subject: Word, predicate: Verb) -> bool:
        '''Определяет, является ли пара слов подлежащим и сказуемым'''
        if WordUtils.is_subject_based_pronoun(subject):
            return subject.number == predicate.number or predicate.infinitive
        if WordUtils.is_nominative_noun(subject):
            return (
                subject.number == predicate.number and (
                    subject.gender == predicate.gender or predicate.gender == Gender.Empty
                )
            )
        return WordUtils.is_proper_noun(subject) and predicate.infinitive


    def get_top_subjects(self, top):
        '''Выделение самых встречающихся подлежащих'''
        frequencies = defaultdict(int)

        for sentence in self._sentences:
            for word in sentence:
                if word.part_sentence == PartSentence.Subject:
                    frequencies[word.lemma] = word.frequency

        return sorted(frequencies.items(), key=lambda x: -x[1])[:top]


    def print_top_subjects(self, top_subjects):
        print('\n'.join([
            f'У слова {word} количество вхождений равно {count}' for word, count in top_subjects
        ]))

    def print_document_links(self):
        print('Подлежащее -> сказуемое')
        for sentence in self._sentences:
            self.print_sentence_links(sentence)

    def print_sentence_links(self, sentence):
        print('Начало предложения')
        for word in sentence:
            for link in word.links:
                print(f'{word.word} ({word.lemma}) -> {link.word} ({link.lemma})')
        print('Конец предложения')


    def pipeline(self):
        '''Общая процедура запуска основной программы'''
        self.parse_text()
        self.prepare_tokens()
        self.define_document_part_sentence()
        self.replace_lemmas_for_pronouns()
        self.calculate_frequencies()
        self.set_subject_object()
        self.print_top_subjects(self.get_top_subjects(3))
        self.print_document_links()