"""Содержит функции для обработки ключей консоли и настройки"""
from typing import List
from os import path
from Spellchecker.conf import *
from Spellchecker.dictExplorer import DictationExplorer

_ERROR_ARGS_STRING = 'Неверные аргументы! Используйте -h, --help для справки'


def _help_view():
    with open('README.md') as f:
        print(f.read())

    return True


def _speed_flag():
    configuration.speed_flag = True


def _add_word(*words):
    if len(words) == 0:
        raise TypeError

    dict_exp = DictationExplorer(configuration.dictation_name)
    for word in words:

        try:
            dict_exp.add_word(word)
            print('Cлова успешно добавлено')

        except AttributeError:
            print(f'Слово {word} уже в словаре')

    return True


_command_dict = {
    '-help': _help_view,
    'h': _help_view,
    '-speed': _speed_flag,
    's': _speed_flag,
    '-add': _add_word
}


def exec_command(conf: Configuration, args: List[str]) -> bool:
    """
    Настраивает работу программы по ключам
    Возвращает True, если программа должна завершиться
    """
    global configuration
    configuration = conf

    if len(args) == 0:
        print(_ERROR_ARGS_STRING)
        return True

    if path.isfile(args[-1]):
        args = args[:-1]

    if len(args) == 0:
        return False

    arg = args[0]

    if not arg.startswith('-'):
        print(_ERROR_ARGS_STRING)
        return True

    arg = arg[1:]

    if arg.startswith('-'):
        try:
            return _command_dict[arg](*args[1:])

        except KeyError:
            print(_ERROR_ARGS_STRING)
            return True

        except TypeError:
            print(_ERROR_ARGS_STRING)
            return True

        except AttributeError as e:
            print(f'Слова {",".join(e.args)} уже есть в словаре')
            return True

    else:
        for a in arg:
            try:
                return _command_dict[a]()

            except KeyError:
                print(_ERROR_ARGS_STRING)
                return True
