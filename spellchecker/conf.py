"""Содержит класс для работы с настройками"""


class Configuration:
    """Класс для хранения параметров программы"""
    def __init__(self, dictation_name: str):
        self.speed_flag = False
        self.dictation_name = dictation_name
