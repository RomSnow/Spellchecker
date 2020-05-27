"""Содержит класс для работы с настройками"""


class Configuration:
    """Класс для хранения параметров программы"""
    def __init__(self, text_name: str, dictation_name: str,
                 is_add_mode=False, is_create_mode=False,
                 items=None):
        if items is None:
            items = []
        self.text_name = text_name
        self.dictation_name = dictation_name
        self.is_add_mode = is_add_mode
        self.is_create_mode = is_create_mode
        self.items = items
