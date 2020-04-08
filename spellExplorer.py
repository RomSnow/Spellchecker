from collections import Generator
from difflib import SequenceMatcher


class SpellExplorer:
    """Содержит инструменты для поиска верного написания слова"""

    @property
    def substitution_words(self) -> tuple:
        return tuple(t[0] for t in self._substitution_words)

    def __init__(self, incorrect_word: str):
        self._count_substitution_words = 5
        self._word = incorrect_word
        self._substitution_words = list()

    def check_for_similarity(self, word_to_check: str):
        """
        Сравнивает слова на схожесть, обновляет наиболее подходящее на замену
        """
        diff_index = SequenceMatcher(None, self._word, word_to_check) \
            .ratio()
        if not self._substitution_words:
            self._substitution_words.append((word_to_check, diff_index))

        for word, di in self._substitution_words:
            if diff_index > di:
                self._substitution_words.append((word_to_check, diff_index))
            sorted(self._substitution_words)
            if len(self._substitution_words) > self._count_substitution_words:
                self._substitution_words.pop(0)
