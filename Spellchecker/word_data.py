"""Содержит класс для хранения атрибутов слова"""


class WordData:
    """Класс для хранения данных слова"""
    def __init__(self, word_code: int, popular_index: float):
        self.word_code = word_code
        self.popular_index = popular_index
