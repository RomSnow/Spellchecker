"""Тесты на работу словаря"""
import unittest
import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                             os.path.pardir))
from spellchecker.dict_explorer import DictationExplorer
from spellchecker.levenshtein_distance import *

CORRECT_WORDS = ('мама', 'дом', 'помощь', 'нужда', 'пламя')
INCORRECT_WORDS = ('мома', 'дйм', 'посмщь', 'нежда', 'плмя')
LEVENSHTEIN_DIST = (1, 1, 2, 1, 1)


class DictTests(unittest.TestCase):
    dict_exp = DictationExplorer(
        '/home/IRD-PC/Projects/Python/Spellchecker/Dictionaries/russian_dict.txt'
    )

    def test_check_word_in_dict(self):
        """Проверяет корректность нахождения слова в словаре"""
        for w in CORRECT_WORDS:
            self.assertTrue(self.dict_exp.check_word_in_dict(w),
                            f'Слово не в словаре {w}')

        for w in INCORRECT_WORDS:
            self.assertFalse(self.dict_exp.check_word_in_dict(w),
                             f'Сработало неверное слово {w}')

    def test_find_similar_word(self):
        """Проверка на коррекстность поиска похожих слов"""
        for i in range(len(INCORRECT_WORDS)):
            self.assertTrue(
                CORRECT_WORDS[i] in self.dict_exp.
                find_most_similar_words(INCORRECT_WORDS[i]),
                f'Для слова {INCORRECT_WORDS[i]} найдено'
                f' {self.dict_exp.find_most_similar_words(INCORRECT_WORDS[i])}'
            )

    def test_levenshtein_distance(self):
        """Проверка работы алгоритма Левенштейна"""
        for i, word in enumerate(INCORRECT_WORDS):
            self.assertEqual(levenshtein_distance(word, CORRECT_WORDS[i]),
                             LEVENSHTEIN_DIST[i])


if __name__ == '__main__':
    unittest.main()
