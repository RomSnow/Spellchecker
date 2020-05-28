"""Содержит функции для обработки ключей консоли и настройки"""
import argparse
import sys
import os

from spellchecker.conf import Configuration


class ArgsParser:
    """Класс для обработки консольных аргументов"""

    def __init__(self, argv):
        self._argv = argv
        self._parser = argparse.ArgumentParser(
            description='Console spellchecker',
            prog='cmain'
        )
        self.add_functions()

    def add_functions(self):
        self._parser.add_argument(
            'text', action='store', nargs='?',
            help='Set name of the file with text to check'
        )
        self._parser.add_argument(
            '-d', action='store', metavar='dict_file',
            default=f'{os.path.dirname(__file__)}'
                    f'/../Dictionaries/russian_dict.dict',
            help='Set name of dictation file (.dict only)'
        )
        self._parser.add_argument(
            '--create', action='store', nargs=2,
            metavar='',
            help='Create new dictation from text [text_name] [out_file_name]'
        )
        self._parser.add_argument(
            '--add', action='store', nargs='+',
            metavar='word',
            help='Add words to standard dictionary'
        )

    def parse(self) -> Configuration:
        data = self._parser.parse_args(args=self._argv)
        items = []
        is_add = False
        is_create = False

        if data.add is not None:
            is_add = True
            items = [*data.add]
        elif data.create is not None:
            is_create = True
            items = [*data.create]

        return Configuration(data.text, data.d,
                             is_add, is_create, items)
