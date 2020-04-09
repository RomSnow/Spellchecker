import sys

from dictExplorer import DictationExplorer
from documentViewer import DocumentViewer


def main():
    text_file, *args = sys.argv[1:]
    dict_exp = DictationExplorer('Dictionaries/russian_dict.txt')
    doc_view = DocumentViewer(text_file)
    string_num = 0
    for words in doc_view.words_on_line:
        string_num += 1
        for word in words:
            if dict_exp.check_word_in_dict(word):
                continue
            substitution_words = dict_exp.find_most_similar_words(word)
            print(f'{word} ?--> {" ".join(substitution_words)}'
                  f' на строке {string_num}')


if __name__ == '__main__':
    main()
