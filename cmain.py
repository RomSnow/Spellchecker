"""Реализация консольной версии программы Spellchecker

Для получения информации по использованию программы
следует обратиться к справке -h, --help"""
import sys

from spellchecker.conf import Configuration
from spellchecker.dict_explorer import DictationExplorer
from spellchecker.document_viewer import DocumentViewer
from spellchecker.console_commands import exec_command


def main():
    """Main function"""
    args = sys.argv[1:]
    conf = Configuration("Dictionaries/russian_dict.txt")
    if exec_command(conf, args):
        return

    text_file = args[len(args) - 1]
    try:
        dict_exp = DictationExplorer(conf.dictation_name)
        doc_view = DocumentViewer(text_file)
    except FileNotFoundError:
        print('Файл не найден')
        return

    string_num = 0
    for words in doc_view.words_on_line:
        string_num += 1

        for word in words:

            if dict_exp.check_word_in_dict(word):
                continue

            substitution_words = dict_exp.find_most_similar_words(
                word, conf.speed_flag
            )
            print(f'{word} ?--> ({" ".join(substitution_words)})'
                  f' на строке {string_num}')


if __name__ == '__main__':
    main()
