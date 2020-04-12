import sys

from Spellchecker.Settings import Settings
from Spellchecker.dictExplorer import DictationExplorer
from Spellchecker.documentViewer import DocumentViewer
from Spellchecker.consoleComands import exec_command


def main():
    args = sys.argv[1:]
    settings = Settings()

    if exec_command(settings, args):
        return

    text_file = args[len(args) - 1]
    try:
        dict_exp = DictationExplorer('Dictionaries/russian_dict.txt')
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

            substitution_words = dict_exp.find_most_similar_words(word)
            print(f'{word} ?--> ({" ".join(substitution_words)})'
                  f' на строке {string_num}')


if __name__ == '__main__':
    main()
