from spellExplorer import SpellExplorer


class DictationExplorer:
    """Содержит интсрументарий для работы со словарем"""

    def __init__(self, dict_file: str):
        self._dict_file = dict_file
        self._words_dict = set()
        with open(dict_file, 'r') as f:
            for line in f:
                self._words_dict.add(line.strip('\n'))

    def check_word_in_dict(self, search_word: str) -> bool:
        """Проверяет вхождение слова в словарь"""
        for dict_word in self._words_dict:
            if search_word == dict_word:
                return True
        return False

    def find_most_similar_words(self, incorrect_word: str) -> tuple:
        """Находит наиболее схожее с исходным слово из словаря"""
        word_exp = SpellExplorer(incorrect_word)
        for dict_word in self._words_dict:
            word_exp.check_for_similarity(dict_word)
        return word_exp.substitution_words

    def add_word(self, word: str):
        """Добавление новго слова в словарь"""
        self._words_dict.add(word)
        with open(self._dict_file, 'a') as f:
            f.writelines([word])
