"""Включает в себя класс для взаимодействия со словарем"""
from multiprocessing import Queue

from progress.bar import Bar

from Spellchecker.fbtrie import Trie
from Spellchecker.file_manager import FileManager


class DictationExplorer(FileManager):
    """Содержит интсрументарий для работы со словарем"""

    def __init__(self, dict_file: str):
        self._dict_file = dict_file
        self._words_fb = Trie()
        self._words_dict = dict()
        self.bar = Bar('Load Dictionary', max=self.count_lines(dict_file))

        with open(dict_file, 'r', encoding='utf-8') as file:
            for line in file:

                line_data = line.strip('\n').split(':')

                if line_data[1] is None or line_data[1] == '':
                    raise AttributeError

                self._words_fb.insert(line_data[0])
                self._words_dict[line_data[0]] = float(line_data[1])
                self.bar.next()

        self.bar.finish()

    def check_word_in_dict(self, search_word: str) -> bool:
        """Проверяет вхождение слова в словарь"""
        return search_word in self._words_dict

    def multiproc_fmsw(self, incorrect_word: str,
                       count: int, queue: Queue, line: int):
        """Оболочка для использования при многопроцессной реализации"""
        queue.put((self.find_most_similar_words(incorrect_word, count),
                   incorrect_word, line))

    def find_most_similar_words(self, incorrect_word: str,
                                count: int) -> tuple:
        """Находит наиболее схожее с исходным слово из словаря"""
        found = self._words_fb.fuzzy(incorrect_word, 2)
        return self._get_most_popular(set(found), count)

    def add_words(self, words: list):
        """Добавление новых слов в словарь"""
        for word in words:
            self._add_word(word)
        print('Words added!')

    def _add_word(self, word: str):
        if self.check_word_in_dict(word):
            raise AttributeError(word)

        self._words_dict[word] = 0
        self._words_fb.insert(word)

        with open(self._dict_file, 'a', encoding='utf-8') as file:
            file.writelines([f'{word}'])

    def _get_most_popular(self, found_words: iter, count: int) -> tuple:
        pop_words = list()

        for word_data in found_words:

            pop_words.append(
                (word_data[1], self._words_dict[word_data[0]],
                 word_data[0])
            )

            a = 0
            if word_data[0] == 'мама':
                a += 1

            pop_words = self._sort_words(pop_words)
            if len(pop_words) > count:
                pop_words.pop(-1)

        return tuple(i[2] for i in pop_words)

    def check_stuck_words(self, incorrect_word: str):
        """
        Проверяет на слипшиеся слова

        Если да, то возвращает пару слов,
        если нет, то None.
        """
        for dict_word in filter(lambda _t: self._words_dict[_t] != 0,
                                self._words_dict.keys()):
            if incorrect_word.startswith(dict_word):
                second_word = incorrect_word[len(dict_word):]

                if second_word in self._words_dict:
                    return dict_word, second_word

        return None

    @staticmethod
    def _sort_words(words: list) -> list:
        sorted_list = list()
        mini_list = list()
        for data in sorted(words):

            if len(mini_list) == 0 or data[0] == mini_list[0][0]:
                mini_list.append(data)

            else:
                sorted_list += sorted(mini_list,
                                      key=lambda _t: _t[1],
                                      reverse=True)
                mini_list.clear()

        sorted_list += sorted(mini_list,
                              key=lambda _t: _t[1],
                              reverse=True)
        mini_list.clear()

        return sorted_list
