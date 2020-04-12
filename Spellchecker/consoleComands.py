"""Содержит функции для обработки ключей консоли и настройки"""
from typing import List
from os import path
from Spellchecker.Settings import Settings

_ERROR_ARGS_STRING = 'Неверные аргументы! Используйте -h, --help для справки'
settings = Settings()


def _help_view():
    with open('README.md') as f:
        print(f.read())

    return True


def _speed_flag():
     pass


def _add_word(*words, dict_exp):
    for word in words:

        try:
            dict_exp.add_word(word)

        except AttributeError:
            print(f'Слово {word} уже в словаре')

    print('Cлова успешно добавлено')
    return True


_command_dict = {
    '-help': _help_view,
    'h': _help_view,
    '-speed': _speed_flag,
    's': _speed_flag,
    '-add': _add_word
}


def exec_command(settings: Settings, args: List[str]) -> bool:
    """
    Настраивает работу программы по ключам
    Возвращает True, если программа должна завершиться
    """
    settings = settings

    if len(args) == 0:
        print(_ERROR_ARGS_STRING)
        return True

    if path.isfile(args[-1]):
        args = args[:-1]

    arg = args[0]
    is_exit = False

    if not arg.startswith('-'):
        print(_ERROR_ARGS_STRING)
        return True

    arg = arg[1:]

    if arg.startswith('-'):
        try:
            return _command_dict[arg](*args[1:])
        except KeyError or TypeError:
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
