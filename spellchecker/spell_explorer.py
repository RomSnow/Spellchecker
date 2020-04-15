from spellchecker.levenshtein_distance import levenshtein_distance
from spellchecker.word_data import WordData


class SpellExplorer:
    """Содержит инструменты для поиска верного написания слова"""

    @property
    def substitution_words(self) -> tuple:
        return tuple(t[1] for t in self._substitution_words)

    def __init__(self, incorrect_word: str):
        self._word = incorrect_word
        self._word_code = self._get_word_code(incorrect_word)
        self._count_substitution_words = 5
        self._substitution_words = list()
        self._current_distance = 1000

    @staticmethod
    def _get_word_code(word: str):
        code = 0

        for letter in word:
            code += ord(letter)

        return code

    def check_for_similarity(self, word_to_check: str, word_data: WordData):
        """
        Сравнивает слова на схожесть, обновляет наиболее подходящее на замену
        """
        if abs(len(word_to_check) - len(self._word)) > 3 \
                or abs(self._word_code - word_data.word_code) > 1110:
            return

        diff_distance = levenshtein_distance(word_to_check, self._word)

        if diff_distance > self._current_distance:
            return

        elif diff_distance < self._current_distance:
            self._substitution_words = [
                (word_data.popular_index, word_to_check)
            ]
            self._current_distance = diff_distance

        else:
            self._substitution_words.append(
                (word_data.popular_index, word_to_check)
            )
            self._substitution_words.sort()

        if len(self._substitution_words) > self._count_substitution_words:
            self._substitution_words.pop(0)
