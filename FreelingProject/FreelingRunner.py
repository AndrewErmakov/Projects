from os import path

from KeyWordSearcher import KeyWordSearcher


if __name__ == '__main__':
    a = KeyWordSearcher(path.join(path.dirname(__file__), 'test.txt'))
    a.pipeline()
