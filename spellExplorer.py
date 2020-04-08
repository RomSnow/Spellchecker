from difflib import SequenceMatcher

from wordData import WordData


class SpellExplorer:
    """Содержит инструменты для поиска верного написания слова"""

    @property
    def substitution_words(self) -> tuple:
        return tuple(t[2] for t in self._substitution_words)

    def __init__(self, incorrect_word: str):
        self._count_substitution_words = 5
        self._word = incorrect_word
        self._substitution_words = list()

    def check_for_similarity(self, word_to_check: WordData):
        """
        Сравнивает слова на схожесть, обновляет наиболее подходящее на замену
        """
        diff_index = SequenceMatcher(None, self._word, word_to_check.word) \
            .ratio()
        if word_to_check.word == 'мама':
            print('мама', word_to_check.popular_index, diff_index)
        if not self._substitution_words:
            self._substitution_words.append(
                (word_to_check.popular_index, diff_index, word_to_check.word)
            )

        for pop_index, di, word in self._substitution_words:
            self._substitution_words.sort()
            if len(self._substitution_words) > self._count_substitution_words:
                self._substitution_words.pop(0)
            if diff_index > di:
                self._substitution_words.append(
                    (word_to_check.popular_index,
                     diff_index, word_to_check.word)
                )
                break
