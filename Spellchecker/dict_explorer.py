"""Включает в себя класс для взаимодействия со словарем"""
from Spellchecker.word_data import WordData
from Spellchecker.spell_explorer import SpellExplorer


class DictationExplorer:
    """Содержит интсрументарий для работы со словарем"""

    def __init__(self, dict_file: str):
        self._dict_file = dict_file
        self._words_dict = dict()
        with open(dict_file, 'r') as file:
            for line in file:
                line_data = line.strip('\n').split(':')
                word_data = WordData(int(line_data[1]), float(line_data[2]))
                self._words_dict[line_data[0]] = word_data

        self._words_dict_lite = frozenset(
            filter(lambda _t: self._words_dict[_t].popular_index > 0,
                   self._words_dict)
        )

    def check_word_in_dict(self, search_word: str) -> bool:
        """Проверяет вхождение слова в словарь"""
        for dict_word in self._words_dict:

            if search_word == dict_word:
                return True

        return False

    def find_most_similar_words(self, incorrect_word: str,
                                speed_flag=False) -> tuple:
        """Находит наиболее схожее с исходным слово из словаря"""
        word_exp = SpellExplorer(incorrect_word)

        if speed_flag:
            current_dict = self._words_dict_lite
        else:
            current_dict = self._words_dict

        for dict_word in current_dict:
            word_exp.check_for_similarity(dict_word,
                                          self._words_dict[dict_word])

        return word_exp.substitution_words

    def add_word(self, word: str):
        """Добавление новго слова в словарь"""
        if self.check_word_in_dict(word):
            raise AttributeError(word)

        self._words_dict[word] = WordData(0, 0)

        with open(self._dict_file, 'a') as file:
            file.writelines([f'{word}:0:0'])
