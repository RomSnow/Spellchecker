"""Содержит класс для работы с текстом"""
import re
from os import path

from spellchecker.file_manager import FileManager


class DocumentViewer(FileManager):
    """Содержит инструментарий для работы с текстом"""

    def __init__(self, text_name: str):
        self._text_name = text_name
        self._words_sep = re.compile(r'[a-zA-Zа-яА-Яё]*[-a-zA-Zа-яА-Я]?')
        self._lines_count = 0

        if not path.isfile(self._text_name):
            raise FileNotFoundError

    def _get_lines(self):
        with open(self._text_name, 'r', encoding='utf-8') as file:
            for line in file:
                yield line

    @property
    def words_on_line(self) -> list:
        for line in self._get_lines():
            yield filter(
                lambda s: s != '',
                map(lambda s: s.lower(), re.findall(self._words_sep, line))
            )

    @property
    def lines_count(self) -> int:
        return self.count_lines(self._text_name)
