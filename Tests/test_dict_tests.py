"""Тесты на работу словаря"""
import subprocess
import sys
import unittest
import os

sys.path.append(os.path.dirname(__file__) + '/..')

import spellchecker.console_commands as c_com
import spellchecker.document_viewer as dv
import spellchecker.dict_creator as dc
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

    def test_console_args(self):
        parser = c_com.ArgsParser([
            '-d', '/Dictionaries/russian_dict.dict', 'text.txt'
        ])
        conf = parser.parse()
        self.assertTrue(
            conf.text_name == 'text.txt' and
            conf.dictation_name == '/Dictionaries/russian_dict.dict' and
            not conf.is_add_mode and
            not conf.is_create_mode and
            conf.items == []
        )

    def test_doc_view(self):
        doc = dv.DocumentViewer(os.path.dirname(__file__) + '/test_text.txt')
        good_ans = ('привет', '-', 'пока', 'вы', 'здесь', '-', 'я', 'тут')
        for words in doc.words_on_line:
            for index, word in enumerate(words):
                self.assertEqual(
                    word, good_ans[index]
                )

    def test_dict_creator(self):
        creator = dc.DictationCreator()
        creator.create('test_text.txt', 'out_dict')
        with open('out_dict.dict') as out:
            with open('normal_dict.dict') as normal:
                self.assertEqual(normal.read(), out.read())

        os.remove('out_dict.dict')


if __name__ == '__main__':
    unittest.main()
