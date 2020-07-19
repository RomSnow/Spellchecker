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


def process_text(doc_view, dict_exp):
    processes = list()
    proc_queue = Queue(maxsize=100)
    found_words = list()

    line_bar = Bar('Text Processing', max=doc_view.lines_count)
    for line_index, words in enumerate(doc_view.words_on_line):
        process_line(words, dict_exp, found_words,
                     line_index, proc_queue, processes)
        line_bar.next()

    line_bar.finish()
    print()

    for proc in processes:
        found_words.append(proc_queue.get())
        proc.join()

    return found_words


def process_line(words_on_line, dict_exp,
                 found_words, line_index,
                 proc_queue, processes):
    for word in words_on_line:

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


def main():
    """Main function"""
    parser = ArgsParser(sys.argv[1:])
    conf = parser.parse()

    if conf.is_create_mode:
        dict_creator = DictationCreator()
        dict_creator.create(*conf.items)
        return

    if conf.text_name is None:
        print('Не указан файл для проверки. '
              'Для справки воспользуйтесь -h, --help')
        return 1

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

    found_words = process_text(doc_view, dict_exp)
    for word_data in sorted(found_words,
                            key=lambda _t: _t[2]):
        print(f"{word_data[1]} ?--> ({', '.join(word_data[0])}) "
              f"на строке {word_data[2]}")


if __name__ == '__main__':
    main()
