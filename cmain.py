"""Реализация консольной версии программы Spellchecker

Для получения информации по использованию программы
следует обратиться к справке -h, --help"""
import sys
from multiprocessing import Process, Queue

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
    for line_index, words in enumerate(doc_view.words_on_line):

        for word in words:

            if dict_exp.check_word_in_dict(word):
                continue

            proc = Process(target=dict_exp.multiproc_fmsw,
                           args=(word, 5, proc_queue))
            proc.start()
            processes.append((proc, word, line_index + 1))

    for proc_data in processes:
        print(f"{proc_data[1]} ?--> ({', '.join(proc_queue.get())}) "
              f"на строке {proc_data[2]}")
        proc_data[0].join()


if __name__ == '__main__':
    main()
