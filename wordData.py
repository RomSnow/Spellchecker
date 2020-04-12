"""WordData - класс, для хранения данных слова"""


class WordData:
    def __init__(self, word_code: int, popular_index: float):
        self.word_code = word_code
        self.popular_index = popular_index
