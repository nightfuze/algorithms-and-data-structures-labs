"""
Задана рекуррентная функция. Область определения функции – натуральные числа.
Написать программу сравнительного вычисления данной функции рекурсивно и итерационно.
Определить границы применимости рекурсивного и итерационного подхода.
Результаты сравнительного исследования времени вычисления представить в табличной и графической форме.

F(x < 2) = 5
F(n) = (-1)^n * (F(n-1) / n! * F(n-5) / (2n)!)
"""

import csv
import time
from decimal import Decimal
from typing import List, Callable, Tuple, Union

from matplotlib import pyplot as plt

BenchData = Tuple[str, List[float]]

fact_cache = {0: 1, 1: 1}
rec_cache = {}


def fact_rec(n: int) -> int:
    """
    Возвращает факториал числа n, используя рекурсию.
n
    :param n: число
    """

    if n < 0:
        raise ValueError("Факториал отрицательного числа не определен")

    if n < 2:
        return 1
    return n * fact_rec(n - 1)


def fact_rec_memo(n: int) -> int:
    """
    Возвращает факториал числа n, используя рекурсию с применением кэширования.

    :param n: число
    """

    if n < 0:
        raise ValueError("Факториал отрицательного числа не определен")

    if n not in fact_cache:
        fact_cache[n] = n * fact_rec_memo(n - 1)

    return fact_cache[n]


def fact_iter(n: int) -> int:
    """
    Возвращает факториал числа n, используя итерацию.

    :param n: число
    """

    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def f_rec(n: int) -> Union[float, int]:
    """
    Возвращает значение функции в точке n, используя рекурсию.

    :param n: точка
    """

    def wrapper(arg: int) -> Union[float, int]:
        if arg < 2:
            return 5
        return wrapper(arg - 1) / fact_rec(arg) * wrapper(arg - 5) / fact_rec(2 * arg)

    return ((-1) ** n) * wrapper(n)


def f_rec_memo(n: int) -> Union[float, int]:
    """
    Возвращает значение функции в точке n, используя рекурсию с применением кэширования.

    :param n: точка
    """

    def wrapper(arg: int) -> Union[float, int]:
        if arg < 2:
            rec_cache[arg] = 5

        if arg not in rec_cache:
            rec_cache[arg] = Decimal(wrapper(arg - 1)) / Decimal(fact_rec_memo(arg)) * Decimal(
                wrapper(arg - 5)) / Decimal(fact_rec_memo(2 * arg))

        return rec_cache[arg]

    return ((-1) ** n) * wrapper(n)


def f_iter(n) -> Union[float, int]:
    """
    Возвращает значение функции в точке n, используя итерацию.

    :param n: точка
    """

    if n < 2:
        return 5

    lst: List[Union[float, int, Decimal]] = [5] * 5

    for i in range(2, n + 1):
        last = lst.pop()
        prev = lst[0]
        lst.insert(0, (Decimal(prev) / Decimal(fact_iter(i))) * Decimal(last) / Decimal(fact_iter(2 * i)))

    return ((-1) ** n) * lst[0]


def display_plot(*bench_data: BenchData, range_lst: List[int]) -> None:
    """
    Выводит график зависимости времени выполнения функции от значения аргумента.

    :param bench_data: кортеж (имя функции, список из времени выполнения функции)
    :param range_lst: список значений аргумента
    """

    for tpl in bench_data:
        plt.plot(range_lst, tpl[1], marker="o", label=tpl[0])

    plt.xlabel("Значение аргумента")
    plt.ylabel("Время выполнения (сек)")
    plt.grid(True)
    plt.legend()
    plt.show()


def write_csv(*bench_data: BenchData, range_lst: List[int], filename: str = "bench") -> None:
    """
    Записывает данные в csv файл.

    :param bench_data: кортеж (имя функции, список времени выполнения функции)
    :param range_lst: список значений аргумента
    :param filename: имя csv файла
    """
    try:
        with open(f"{filename}.csv", "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                [
                    "n Аргумент функции",
                    *[
                        f"Время выполнения функции {tpl[0]}(n) в секундах"
                        for tpl in bench_data
                    ],
                ]
            )

            for i, n in enumerate(range_lst):
                row = [n]
                for tpl in bench_data:
                    row.append(format(tpl[1][i], ".10f"))
                writer.writerow(row)

        print(f"Данные записаны в файл {filename}.csv")

    except Exception as e:
        print(f"Невозможно записать данные в файл. Ошибка: {e}")


def bench_func(func: Callable[[int], int], arg: int) -> float:
    """
    Возвращает время выполнения функции func(arg) в секундах.

    :param func: функция
    :param arg: аргумент функции
    """

    start = time.perf_counter()
    func(arg)
    end = time.perf_counter()
    return end - start


def get_bench_data(func: Callable[[int], int], range_lst: List[int]) -> BenchData:
    """
    Возвращает кортеж (имя функции, список времени выполнения функции).

    :param func: функция
    :param range_lst: список значений аргумента
    """

    return func.__name__, [bench_func(func, n) for n in range_lst]


def get_input(text: str) -> int:
    """
    Возвращает ввод пользователя.

    :param text: текст запроса
    """
    while True:
        try:
            value = int(input(text))
            return value
        except ValueError:
            print("Ошибка: Значение должно быть целым. Попробуйте еще раз.")


def get_valid_input(text: str, min_val: int = 2, max_val: int = 500) -> int:
    """
    Возвращает ввод пользователя, проверяя его на валидность.

    :param min_val: минимальное значение
    :param max_val: максимальное значение
    :param text: текст запроса
    """
    while True:
        try:
            value = get_input(text)
            if value > max_val or value < min_val:
                raise ValueError
            return value
        except ValueError:
            print(f"Ошибка: Значение должно быть от {min_val} до {max_val}. Попробуйте еще раз.")


def run_bench(k: int):
    """
    Функция для вывода графиков времени выполнения функции и записи результатов в csv файл.
    Используется рекурсия без оптимизации.

    :param k: размер последовательности натуральных чисел
    """

    # Так как используется рекурсия без оптимизации, то уменьшаем k до 30, иначе превышает глубину рекурсии
    if k > 30:
        k = 30

    natural_numbers = [i for i in range(1, k + 1)]
    iter_data = get_bench_data(f_iter, natural_numbers)
    rec_data = get_bench_data(f_rec, natural_numbers)
    display_plot(iter_data, rec_data, range_lst=natural_numbers)
    write_csv(iter_data, rec_data, range_lst=natural_numbers, filename="bench")


def run_bench_memo(k: int):
    """
    Функция для вывода графиков времени выполнения функции и записи результатов в csv файл.
    Используется рекурсия с оптимизацией.

    :param k: размер последовательности натуральных чисел
    """

    natural_numbers = [i for i in range(1, k + 1)]
    rec_data = get_bench_data(f_rec_memo, natural_numbers)
    iter_data = get_bench_data(f_iter, natural_numbers)
    display_plot(iter_data, rec_data, range_lst=natural_numbers)
    write_csv(iter_data, rec_data, range_lst=natural_numbers, filename="bench_memo")


def main():
    k = get_valid_input("K = ")

    run_bench(k)
    run_bench_memo(k)


if __name__ == "__main__":
    main()
