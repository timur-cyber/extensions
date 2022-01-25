"""
Программа работающая как классический t9, подбирая слова из введённого набора цифр
"""
from typing import List

keyboard = {
    '2': ('a', 'b', 'c'),
    '3': ('d', 'e', 'f'),
    '4': ('g', 'h', 'i'),
    '5': ('j', 'k', 'l'),
    '6': ('m', 'n', 'o'),
    '7': ('p', 'q', 'r', 's'),
    '8': ('t', 'u', 'v'),
    '9': ('w', 'x', 'y', 'z')
}


def my_t9(input_numbers: str) -> List[str]:
    numbers = [num for num in input_numbers]
    key_values = []
    words = []
    for num in numbers:
        key_values.append(keyboard[num])
    with open('/usr/share/dict/words', 'r', encoding='utf-8') as file:
        for word in file:
            word = word.replace('\n', '')
            if len(word) == len(input_numbers):
                compatibility = []
                for i in range(len(input_numbers)):
                    for letter in key_values[i]:
                        if letter == word[i]:
                            compatibility.append(True)
                            break

                if len(compatibility) == len(input_numbers) and all(compatibility):
                    words.append(word)

    return words


print(my_t9(input('Введите набор цифр -> ')))
