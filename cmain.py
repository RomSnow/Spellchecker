from dictExplorer import DictationExplorer


def main():
    exp = DictationExplorer('Dictionaries/russian.txt')
    print(exp._words_dict)


if __name__ == '__main__':
    main()
