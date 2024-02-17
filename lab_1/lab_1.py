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


def replace_first_digit(number: int) -> str:
    first_digit: str = str(abs(number))[0]
    return str(number).replace(first_digit, digit_word[int(first_digit)], 1)


def extract_integers(word: str) -> List[int]:
    integers: List[int] = []

    current_number: str = ''
    is_float: bool = False

    for char in word:
        if char.isdigit() and not is_float:
            current_number += char
        elif char == '.':
            current_number = ''
            is_float = True
        elif current_number and not is_float:
            integers.append(int(current_number))
            current_number = ''
        elif not char.isdigit() and is_float:
            current_number = ''
            is_float = False

    if current_number:
        integers.append(int(current_number))

    return integers


def process_file(file_name: str, buffer_size: int) -> List[str]:
    try:
        result: List[str] = []

        with open(file_name, 'r') as file:
            while True:
                buffer: str = file.read(buffer_size)
                if not buffer:
                    break
                lexemes_list: List[str] = buffer.split()
                for lexeme_index, lexeme_item in enumerate(lexemes_list):
                    numbers: List[int] = extract_integers(lexeme_item)
                    for number in numbers:
                        if number % 2 == 0:
                            replaced_number: str = replace_first_digit(number)
                            result.append(replaced_number)
                        else:
                            result.append(str(number))
        return result
    except FileNotFoundError:
        print("Файл не найден")


def lab_1():
    buffer_size: int = 32
    file_name: str = "input.txt"
    result = process_file(file_name, buffer_size)
    print(*result)


lab_1()
