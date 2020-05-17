"""Включает в себя класс для взаимодействия со словарем"""
from Spellchecker.fbtrie import FBTrie


class DictationExplorer:
    """Содержит интсрументарий для работы со словарем"""

    def __init__(self, dict_file: str):
        self._dict_file = dict_file
        self._words_fb = FBTrie()
        self._words_dict = set()
        with open(dict_file, 'r', encoding='utf-8') as file:
            for line in file:
                line_data = line.strip('\n').split(':')
                self._words_fb.insert(line_data[0])
                self._words_dict.add(line_data[0])

    def check_word_in_dict(self, search_word: str) -> bool:
        """Проверяет вхождение слова в словарь"""
        return search_word in self._words_dict

    def find_most_similar_words(self, incorrect_word: str,
                                count: int) -> tuple:
        """Находит наиболее схожее с исходным слово из словаря"""
        found = self._words_fb.fuzzy(incorrect_word, 1)
        return tuple(
            i[0] for i in sorted(found, key=lambda _t: _t[1])
        )[:count]

    def add_word(self, word: str):
        """Добавление новго слова в словарь"""
        if self.check_word_in_dict(word):
            raise AttributeError(word)

        self._words_dict.add(word)
        self._words_fb.insert(word)

        with open(self._dict_file, 'a', encoding='utf-8') as file:
            file.writelines([f'{word}'])
