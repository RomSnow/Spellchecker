class WordData:
    """Структура для хранения данных о слове"""

    def __init__(self, word: str, popular_index: float):
        self.word = word
        self.popular_index = popular_index
