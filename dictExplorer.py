class DictationExplorer:
    """Содержит интсрументарий для работы со словарем"""

    def __init__(self, dict_file: str):
        self._dict_file = dict_file
        self._words_dict = set()
        with open(dict_file, 'r') as f:
            for line in f:
                self._words_dict.add(line)

    def add_word(self, word: str):
        """Добавление новго слова в словарь"""
        self._words_dict.add(word)
        with open(self._dict_file, 'w') as f:
            f.writelines([word])
