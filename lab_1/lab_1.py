# Написать программу, которая читая символы из бесконечной последовательности
# (эмулируется конечным файлом, читающимся поблочно), распознает, преобразует и выводит на экран лексемы
# по определенному правилу. Лексемы разделены пробелами. Преобразование делать по возможности через словарь.
# Для упрощения под выводом числа прописью подразумевается последовательный вывод всех цифр числа.
# Регулярные выражения использовать нельзя.
# Целые нечетные числа. Замена: первая цифра каждого четного числа на нечетном месте на английскую цифру прописью.
from typing import List

digit_word = {
    0: "zero",
    1: "one",
    2: "two",
    3: "three",
    4: "four",
    5: "five",
    6: "six",
    7: "seven",
    8: "eight",
    9: "nine"
}


def replace_digits(number: int) -> str:
    digits: str = str(number)

    is_replaced = False
    for index, digit in enumerate(digits):
        # Замена первой цифры четного числа на нечетном месте на английскую цифру прописью
        if number % 2 == 0 and (index + 1) % 2 != 0 and not is_replaced:
            digits = digits.replace(digit, digit_word[int(digit)], 1)
            is_replaced = True
    return digits


def extract_integers(word: str) -> List[int]:
    integers: List[int] = []

    current_int: int = 0
    is_float: bool = False

    for char in word:
        if char.isdigit() and not is_float:
            current_int = current_int * 10 + int(char)
        elif char == '.':
            current_int = 0
            is_float = True
        elif current_int != 0 and not is_float:
            integers.append(current_int)
            current_int = 0
        elif not char.isdigit() and is_float:
            is_float = False

    if current_int != 0:
        integers.append(current_int)

    return integers


def process_file(file_name: str, buffer_size: int) -> List[str]:
    try:
        lexemes: List[str] = []

        with open(file_name, 'r') as file:
            while True:
                buffer: str = file.read(buffer_size)
                if not buffer:
                    break
                char_list: List[str] = buffer.split()
                # print("initial char_list:", char_list)
                for char_index, char_item in enumerate(char_list):
                    numbers: List[int] = extract_integers(char_item)
                    # print("numbers:", numbers)
                    for number in numbers:
                        number_in_word: str = replace_digits(number)
                        char_list[char_index] = char_item.replace(str(number), number_in_word)
                lexemes.append(" ".join(char_list))
                # print(" ".join(char_list))
                # print("final char_list:", char_list)

        return lexemes
    except FileNotFoundError:
        print("Файл не найден")


def lab_1():
    buffer_size: int = 4
    file_name: str = "input.txt"
    lexemes = process_file(file_name, buffer_size)
    print(*lexemes)


lab_1()
