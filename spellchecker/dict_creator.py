import re
import sys


class DictationCreator:
    """Класс для создания новых словарей"""

    def __init__(self):
        self.pattern = re.compile(r'[a-zA-Zа-яА-Яё]*[-a-zA-Zа-яА-Я]?')

    def create(self, file_in: str, file_out: str):
        words_dict = dict()

        with open(file_in, 'r') as file:
            for line in file:
                for word in self.pattern.findall(line):
                    word = word.lower()
                    words_dict[word] = \
                        words_dict.setdefault(word, 0) + 1

        words_dict.pop('')
        with open(f'{file_out}.dict', 'w') as file:
            for word, popular in words_dict.items():
                file.write(f'{word}:{popular / len(words_dict) * 10000}\n')

        print(f'Dictation {file_out}.dict created')


if __name__ == '__main__':
    creator = DictationCreator()
    creator.create(sys.argv[1], sys.argv[2])
