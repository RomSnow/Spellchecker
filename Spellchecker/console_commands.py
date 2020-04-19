"""Содержит функции для обработки ключей консоли и настройки"""
from typing import List
from os import path

from Spellchecker.conf import Configuration
from Spellchecker.dict_explorer import DictationExplorer

_ERROR_ARGS_STRING = 'Неверные аргументы! Используйте -h, --help для справки'


def _help_view():
    with open('chelp.txt', 'r', encoding='utf-8') as file:
        print(file.read())

    return True


def _speed_flag():
    CONFIGURATION.speed_flag = True


def _add_words(*words):
    if len(words) == 0:
        raise TypeError

    dict_exp = DictationExplorer(CONFIGURATION.dictation_name)
    for word in words:

        try:
            dict_exp.add_word(word)
            print('Cлова успешно добавлено')

        except AttributeError:
            print(f'Слово {word} уже в словаре')

    return True


# Словарь с ключами
_COMMAND_DICT = {
    '-help': _help_view,
    'h': _help_view,
    '-speed': _speed_flag,
    's': _speed_flag,
    '-add': _add_words
}


def exec_command(conf: Configuration, args: List[str]) -> bool:
    """Настраивает работу программы по ключам

    Возвращает True, если программа должна завершиться"""
    global CONFIGURATION
    CONFIGURATION = conf

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
        return _do_command(arg, args[1:])

    is_exit = False
    for letter in arg:
        is_exit = _do_command(letter, args[1:])
    return is_exit


def _do_command(command: str, args) -> bool:
    """Выполняет действия в соостветсии с ключом"""
    try:
        return _COMMAND_DICT[command](*args)

    except KeyError:
        print(_ERROR_ARGS_STRING)
        return True

    except TypeError:
        print(_ERROR_ARGS_STRING)
        return True

    except AttributeError as expt:
        print(f'Слова {",".join(expt.args)} уже есть в словаре')
        return True
