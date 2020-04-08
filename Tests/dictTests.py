import unittest
from dictExplorer import DictationExplorer

CORRECT_WORDS = ('мама', 'дом', 'помощь', 'нужда', 'пламя')
INCORRECT_WORDS = ('мома', 'дйм', 'посмщь', 'нежда', 'плмя')


class MyTestCase(unittest.TestCase):
    dict_exp = DictationExplorer(
        '/home/IRD-PC/Projects/Python/Spellchecker/Dictionaries/russian_dict.txt'
    )

    def test_add_word(self):
        self.dict_exp.add_word('new_word')
        self.assertTrue(self.dict_exp.check_word_in_dict('new_word'),
                        'Слово не добавлено')

    def test_check_word_in_dict(self):
        for w in CORRECT_WORDS:
            self.assertTrue(self.dict_exp.check_word_in_dict(w),
                            f'Слово не в словаре {w}')
        for w in INCORRECT_WORDS:
            self.assertFalse(self.dict_exp.check_word_in_dict(w),
                             f'Сработало неверное слово {w}')

    def test_find_similar_word(self):
        for i in range(len(INCORRECT_WORDS)):
            self.assertTrue(
                CORRECT_WORDS[i] in self.dict_exp.
                find_most_similar_words(INCORRECT_WORDS[i]),
                f'Для слова {INCORRECT_WORDS[i]} найдено'
                f' {self.dict_exp.find_most_similar_words(INCORRECT_WORDS[i])}'
            )


if __name__ == '__main__':
    unittest.main()
