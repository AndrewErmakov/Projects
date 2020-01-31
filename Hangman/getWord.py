import random
import json
from pprint import pprint


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
        self.current_words = self.read_dict_words()
        print('ДО')
        pprint(self.current_words)
        self.subject_new_word = input("Введите тематику нового слова:")
        self.added_words = input("Введите добавляемое слово(а):").split()

        if self.subject_new_word not in self.current_words:
            self.current_words[self.subject_new_word] = []
            self.extension_vocabulary()

        else:
            self.extension_vocabulary()

        self.update_dict_words(self.current_words)
        print('ПОСЛЕ')
        pprint(self.current_words)

    def extension_vocabulary(self):
        for new_word in self.added_words:
            if new_word not in self.current_words[self.subject_new_word]:
                self.current_words[self.subject_new_word].append(new_word)



