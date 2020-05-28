"""Тесты на работу словаря"""
import subprocess
import sys
import unittest
import os

sys.path.append(os.path.dirname(__file__) + '/..')

from spellchecker.dict_explorer import DictationExplorer

CORRECT_WORDS = ('мама', 'дом', 'помощь', 'нужда', 'пламя')
INCORRECT_WORDS = ('мома', 'дйм', 'посмщь', 'нежда', 'плмя')
LEVENSHTEIN_DIST = (1, 1, 2, 1, 1)


class DictTests(unittest.TestCase):
    dict_exp = DictationExplorer(
        f'{os.path.dirname(__file__)}/../Dictionaries/russian_dict.dict'
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
                find_most_similar_words(INCORRECT_WORDS[i], 3),
                f'Для слова {INCORRECT_WORDS[i]} найдено'
                f' {self.dict_exp.find_most_similar_words(INCORRECT_WORDS[i], 3)}'
            )

    def test_get_most_popular(self):
        l = (('мама', 1), ('дом', 1), ('крыша', 4),
             ('наковальня', 2), ('марионетка', 1), ('империализм', 3))

        self.assertEqual(('дом', 'мама', 'марионетка'),
                         self.dict_exp._get_most_popular(l, 3))

    def test_count_line(self):
        self.assertEqual(int(subprocess.check_output(
            f"wc -l {__file__}",
            shell=True
        ).split()[0]), self.dict_exp.count_lines(__file__))

    def test_stuck_words(self):
        self.assertEqual(
            ('дом', 'лестница'),
            self.dict_exp.check_stuck_words('домлестница')
                         )
        self.assertEqual(
            None,
            self.dict_exp.check_stuck_words('афарокр')
        )


if __name__ == '__main__':
    unittest.main()
