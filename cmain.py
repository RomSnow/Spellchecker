#!./venv/bin/python
"""Реализация консольной версии программы Spellchecker

Для получения информации по использованию программы
следует обратиться к справке -h, --help"""
import sys
from multiprocessing import Process, Queue

from progress.bar import Bar

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

    processes = list()
    proc_queue = Queue()
    found_words = list()

    line_bar = Bar('Text Processing', max=doc_view.lines_count)
    for line_index, words in enumerate(doc_view.words_on_line):

        for word in words:

            if dict_exp.check_word_in_dict(word):
                continue

            stuck_words = dict_exp.check_stuck_words(word)

            if stuck_words is not None:
                found_words.append((
                    stuck_words, word, line_index + 1
                ))
                continue

            proc = Process(target=dict_exp.multiproc_fmsw,
                           args=(word, 5, proc_queue, line_index + 1))
            proc.start()
            processes.append(proc)
        line_bar.next()

    line_bar.finish()
    print()

    for proc in processes:
        found_words.append(proc_queue.get())
        proc.join()

    for word_data in sorted(found_words,
                            key=lambda _t: _t[2]):
        print(f"{word_data[1]} ?--> ({', '.join(word_data[0])}) "
              f"на строке {word_data[2]}")


if __name__ == '__main__':
    main()
