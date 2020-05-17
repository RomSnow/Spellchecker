"""Реализация консольной версии программы Spellchecker

Для получения информации по использованию программы
следует обратиться к справке -h, --help"""
import sys

from Spellchecker.conf import Configuration
from Spellchecker.dict_explorer import DictationExplorer
from Spellchecker.document_viewer import DocumentViewer
from Spellchecker.console_commands import exec_command


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
    out_str = ''
    for line_index, words in enumerate(doc_view.words_on_line):

        for word in words:

            if dict_exp.check_word_in_dict(word):
                continue

            substitution_words = dict_exp.find_most_similar_words(
                word, 5
            )
            out_str += f'{word} ?--> ({" ".join(substitution_words)}) ' \
                       f'на строке {line_index + 1}\n'

    print(out_str)


if __name__ == '__main__':
    main()
