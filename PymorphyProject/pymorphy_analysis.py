import string
from os import path


import pymorphy2


class PymorphyKeyWordSearcher(object):

    def __init__(
            self,
            path_to_text_file,
            language='ru'
    ):
        self._path_to_text_file = path_to_text_file
        self._language = language
        if not path.exists(self._path_to_text_file):
            print('No file in', self._path_to_text_file)
            raise FileNotFoundError

        self._notRecognizedWords = []
        self._dictKeyStruct = {}
        self._dictAllVerbs = {}
        self._averageVerbs = None
        self._averageNouns = None
        self._keyPhrases = []

    def parse_text(self):
        sentences = []
        current_sentence = []

        with open(self._path_to_text_file, 'r', encoding='utf-8') as fp:
            for line in fp:
                tokens = line.strip().split()
                for token in tokens:
                    current_sentence.append(token)
                    if token[-1] in ['.', '?', '!', '…']:
                        sentence = [self.remove_punctuation(token) for token in current_sentence]
                        sentences.append(sentence)
                        current_sentence = []
        return sentences

    def remove_punctuation(self, word):
        for symbol in string.punctuation:
            if symbol != '-':
                word = word.replace(symbol, '')
        return word

    def run_analyzer(self, sentences):
        analyzer = pymorphy2.MorphAnalyzer()
        tagged_sentences = []
        for sentence in sentences:
            tagged_sentence = [analyzer.parse(word)[0] for word in sentence]
            tagged_sentences.append(tagged_sentence)
        return tagged_sentences

    def get_not_recognized_words(self):
        return self._notRecognizedWords

    def get_average_verbs(self):
        if self._averageVerbs == None:
            self.calculate_average_verbs()
        return self._averageVerbs

    def calculate_average_verbs(self):
        if len(self._dictAllVerbs) != 0:
            self._averageVerbs = sum([self._dictAllVerbs[x] for x in self._dictAllVerbs]) / len(self._dictAllVerbs)
        else:
            raise ZeroDivisionError("No verbs")
        return self._averageVerbs

    def is_base(self, noun, verb):
        return noun['case'] == 'nomn' and \
               (noun['gen'] == verb['gen'] or verb['gen'] is None) and \
               (noun['num'] == verb['num'] or noun['num'] is None)

    def calculate_bases(self, sentences):
        for sentence in sentences:
            nouns = []
            verbs = []
            local_sentences = {}
            for token in sentence:
                if token.tag.POS == 'NOUN':
                    nouns.append({
                        'gen': token.tag.gender,
                        'num': token.tag.number,
                        'form': token.word,
                        'lemma': token.normal_form,
                        'case': token.tag.case
                    })
                elif token.tag.POS == 'VERB':
                    verbs.append({
                        'gen': token.tag.gender,
                        'num': token.tag.number,
                        'form': token.word,
                        'lemma': token.normal_form
                    })
                elif token.tag.POS == 'NPRO':
                    nouns.append({
                        'gen': token.tag.gender,
                        'num': token.tag.number,
                        'form': token.word,
                        'lemma': token.normal_form,
                        'case': token.tag.case
                    })
            for verb in verbs:
                for noun in nouns:
                    if self.is_base(noun, verb):
                        print('Base is ', noun['form'], verb['form'])
                        if verb['lemma'] not in local_sentences:
                            local_sentences.update({
                                verb['lemma']: {
                                    'verb': verb['form'],
                                    'noun'
                                    : [noun['form']]
                                }
                            })
                        else:
                            if noun['form'] not in local_sentences[verb['lemma']]['noun']:
                                local_sentences[verb['lemma']]['noun'].append(noun['lemma'])

            for key in local_sentences:
                for noun in local_sentences[key]['noun']:
                    if noun.lower() not in self._dictKeyStruct:
                        self._dictKeyStruct.update(
                            {noun.lower(): {'count': 1, 'verbs': {local_sentences[key]['verb']: 1}}})
                    else:
                        if local_sentences[key]['verb'] not in self._dictKeyStruct[noun.lower()]['verbs']:
                            self._dictKeyStruct[noun.lower()]['verbs'].update({local_sentences[key]['verb']: 1})
                        else:
                            self._dictKeyStruct[noun.lower()]['verbs'][local_sentences[key]['verb']] += 1
                        self._dictKeyStruct[noun.lower()]['count'] += 1

    def calculate_some_statistic(self):
        for key in self._dictKeyStruct:
            self._dictKeyStruct[key]['average'] = sum(
                [self._dictKeyStruct[key]['verbs'][x] for x in self._dictKeyStruct[key]['verbs']]) \
                                                  / len(self._dictKeyStruct[key]['verbs'])
            for item in self._dictKeyStruct[key]['verbs']:
                if item not in self._dictAllVerbs:
                    self._dictAllVerbs.update({item: self._dictKeyStruct[key]['verbs'][item]})
                else:
                    self._dictAllVerbs[item] += self._dictKeyStruct[key]['verbs'][item]
            print('у слова ', key, ' количество вхождений равно', self._dictKeyStruct[key]['count'],
                  'среднее по существительному:',
                  self._dictKeyStruct[key]['average'])
        # trashhold = sum([nlist[x]['count'] for x in nlist]) / sum([[]])

    def calculate_average_nouns(self):
        if len(self._dictKeyStruct) > 0:
            self._averageNouns = sum([self._dictKeyStruct[x]['count'] for x in self._dictKeyStruct]) / len(
                self._dictKeyStruct)
        else:
            raise ZeroDivisionError("No nouns")
        return self._averageNouns

    def prepare_nouns(self, max_count_elements):
        sortedDictKeyStruct = sorted(self._dictKeyStruct.items(), key=lambda kv: kv[1]['count'], reverse=True)
        if max_count_elements < len(sortedDictKeyStruct):
            sortedDictKeyStruct = sortedDictKeyStruct[:max_count_elements]
        return sortedDictKeyStruct

    def prepare_verbs_by_noun(self, noun, maxCountElems):
        sortedVerbs = sorted(self._dictKeyStruct[noun]['verbs'].items(), key=lambda kv: kv[1], reverse=True)[:2]
        if len(sortedVerbs) > maxCountElems:
            sortedVerbs = sortedVerbs[:maxCountElems]
        return sortedVerbs

    def get_key_phrases(self, threshold_noun=1, threshold_verb=1):
        self._keyPhrases.clear()
        for key, value in self.prepare_nouns(4):
            if value['count'] > threshold_noun:
                currentVerbs = self.prepare_verbs_by_noun(key, 2)
                self._keyPhrases.append(str(key) + " " + ",".join(
                    [verb + ":" + str(verb_count) for verb, verb_count in currentVerbs if verb_count > threshold_verb]))
        return self._keyPhrases

    def printResult(self):
        print("-----------------------")
        print('Key phrases in', self._path_to_text_file, 'are:')
        print('\n'.join(self._keyPhrases))
        if len(self._notRecognizedWords) > 0:
            print('Words with errors:', ', '.join(self._notRecognizedWords))
        else:
            print('All words recognized')


if __name__ == '__main__':
    a = PymorphyKeyWordSearcher(path.join(path.dirname(__file__), 'got.txt'))
    sentences = a.parse_text()
    tagged_sentences = a.run_analyzer(sentences)
    a.calculate_bases(tagged_sentences)

    a.get_key_phrases()
    a.printResult()
    a.calculate_some_statistic()
