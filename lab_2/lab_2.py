"""
Написать программу, которая, распознает, преобразует и выводит на экран лексемы по определенному правилу.
Лексемы разделены пробелами. Преобразование делать по возможности через словарь.
Для упрощения под выводом числа прописью подразумевается последовательный вывод всех цифр числа.

Входной файл является обыкновенным (т.е. нет требования на «бесконечность» файла);
Распознавание и обработку делать через регулярные выражения;
В вариантах, где есть параметр (например К), допускается его заменить на любое число;
Все остальные требования соответствуют варианту задания лабораторной работы №1.

Целые нечетные числа. Замена: первая цифра каждого четного числа на нечетном месте на английскую цифру прописью.
"""
import re
from typing import List, Dict

digit_word: Dict[int, str] = {
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
    matches: List[str] = re.findall(r"-?(?<![.\d])\d+(?![.\d])", text)
    return list(map(int, matches))


def process_file(file_name: str) -> None:
    try:
        with open(file_name, 'r') as file:
            read_data: str = file.read()
            lexemes_list: List[str] = re.findall(r'\S+', read_data)
            integers_list: List[int] = extract_integers(" ".join(lexemes_list))
            even_integers_list: List[str] = re.findall(r'-?\b\d*[02468]\b', " ".join(list(map(str, integers_list))))
            odd_integers_list: List[str] = re.findall(r'-?\b\d*[13579]\b', " ".join(list(map(str, integers_list))))
            replaced_even_integers_list: List[str] = list(map(replace_first_digit, list(map(int, even_integers_list))))
            transformed_integers: List[str] = replaced_even_integers_list + odd_integers_list
            print(*transformed_integers)
    except FileNotFoundError:
        print("Файл не найден")


def lab_2():
    file_name: str = "input.txt"
    process_file(file_name)


lab_2()
