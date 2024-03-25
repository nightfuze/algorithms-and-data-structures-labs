import csv
import time
from typing import List, Callable, Tuple, Union

from matplotlib import pyplot as plt

BenchData = Tuple[str, List[float]]


def fact_rec(n: int) -> int:
    """
    Возвращает факториал числа n, используя рекурсию.

    :param n: число
    """

    if n < 2:
        return 1
    return n * fact_rec(n - 1)


def fact_iter(n: int) -> int:
    """
    Возвращает факториал числа n, используя итерацию.

    :param n: число
    """

    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


def f_rec(n: int) -> Union[float, int]:
    """
    Возвращает значение функции в точке n, используя рекурсию.

    :param n: точка
    """

    if n < 2:
        return 5
    return (-1) ** n * (f_rec(n - 1) / fact_rec(n) * f_rec(n - 5) / fact_rec(2 * n))


def f_iter(n) -> Union[float, int]:
    """
    Возвращает значение функции в точке n, используя итерацию.

    :param n: точка
    """

    if n < 2:
        return 5

    lst = [5] * 5

    for i in range(2, n + 1):
        last = lst.pop()
        prev = lst[0]
        lst.insert(0, (-1) ** i * (prev / fact_iter(i)) * last / fact_iter(2 * i))

    return lst[0]


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


def get_valid_input(text: str) -> int:
    """
    Возвращает ввод пользователя, проверяя его на валидность.

    :param text: текст запроса
    
    """
    while True:
        try:
            value = get_input(text)
            if value > 50 or value < 2:
                raise ValueError
            return value
        except ValueError:
            print("Ошибка: Значение должно быть от 2 до 50. Попробуйте еще раз.")


def main():
    k = get_valid_input("K = ")
    natural_numbers = [i for i in range(1, k + 1)]

    iter_data = get_bench_data(f_iter, natural_numbers)
    rec_data = get_bench_data(f_rec, natural_numbers)

    display_plot(iter_data, rec_data, range_lst=natural_numbers)
    write_csv(iter_data, rec_data, range_lst=natural_numbers)


if __name__ == "__main__":
    main()
