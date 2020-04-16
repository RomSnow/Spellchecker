"""Реализация алгоритма Левенштейна для сравнения слов"""


def levenshtein_distance(first_word: str, second_word: str) -> int:
    if len(first_word) < len(second_word):
        return levenshtein_distance(second_word, first_word)

    if len(second_word) == 0:
        return len(first_word)

    previous_row = range(len(second_word) + 1)

    for i, letter_1 in enumerate(first_word):
        current_row = [i + 1]

        for j, letter_2 in enumerate(second_word):
            insertions = previous_row[j + 1] + 1
            deletions = current_row[j] + 1
            substitutions = previous_row[j] + (letter_1 != letter_2)

            current_row.append(min(insertions, deletions, substitutions))

        previous_row = current_row

    return previous_row[-1]
