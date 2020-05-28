#!./venv/bin/python
"""Реализация консольной версии программы spellchecker

Для получения информации по использованию программы
следует обратиться к справке -h, --help"""
import sys
from multiprocessing import Process, Queue

from progress.bar import Bar

from spellchecker.console_commands import ArgsParser
from spellchecker.dict_creator import DictationCreator
from spellchecker.dict_explorer import DictationExplorer
from spellchecker.document_viewer import DocumentViewer


def main():
    """Main function"""
    parser = ArgsParser(sys.argv[1:])
    conf = parser.parse()

    if conf.is_create_mode:
        dict_creator = DictationCreator()
        dict_creator.create(*conf.items)
        return

    try:
        dict_exp = DictationExplorer(conf.dictation_name)
    except FileNotFoundError:
        print(conf.dictation_name)
        print('\nСловарь не найден!')
        return
    except Exception:
        print('\nНекорректный словарь!')
        return

    if conf.is_add_mode:
        dict_exp.add_words(conf.items)
        return

    try:
        doc_view = DocumentViewer(conf.text_name)
    except FileNotFoundError:
        print('\nФайл не найден')
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
