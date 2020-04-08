from dictExplorer import DictationExplorer


def main():
    exp = DictationExplorer('Dictionaries/russian_dict.txt')
    print(exp.find_most_similar_words('мома'))


if __name__ == '__main__':
    main()
