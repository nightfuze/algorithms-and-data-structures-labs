# Написать программу, которая читая символы из бесконечной последовательности
# (эмулируется конечным файлом, читающимся поблочно), распознает, преобразует и выводит на экран лексемы
# по определенному правилу. Лексемы разделены пробелами. Преобразование делать по возможности через словарь.
# Для упрощения под выводом числа прописью подразумевается последовательный вывод всех цифр числа.
# Используя регулярные выражения.
# Целые нечетные числа. Замена: первая цифра каждого четного числа на нечетном месте на английскую цифру прописью.
import re
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


def extract_integers(text: str) -> List[int]:
    matched = re.findall(r'-?\d*\.?\d+', text)
    return [int(x) for x in matched if x.find('.') == -1]


def process_file(file_name: str, buffer_size: int) -> None:
    try:
        with open(file_name, 'r') as file:
            while True:
                result: List[str] = []
                buffer: str = file.read(buffer_size)
                if not buffer:
                    break
                lexemes_list: List[str] = buffer.split()
                for lexeme_item in lexemes_list:
                    numbers: List[int] = extract_integers(lexeme_item)
                    for number in numbers:
                        if number % 2 == 0:
                            replaced_number: str = replace_first_digit(number)
                            result.append(replaced_number)
                        else:
                            result.append(str(number))
                print(*result)
    except FileNotFoundError:
        print("Файл не найден")


def lab_2():
    buffer_size: int = 32
    file_name: str = "input.txt"
    process_file(file_name, buffer_size)


lab_2()
