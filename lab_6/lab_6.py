"""
Задание состоит из двух частей.
1 часть – написать программу в соответствии со своим вариантом задания.
Написать 2 варианта формирования (алгоритмический и с помощью функций Питона), сравнив по времени их выполнение.
2 часть – усложнить написанную программу, введя по своему усмотрению в условие минимум одно ограничение на характеристики объектов
(которое будет сокращать количество переборов)  и целевую функцию для нахождения оптимального  решения.

Вариант 6.
Кафе набирает сотрудников: 2 посудомойки (женщины), 5 грузчиков (мужчины), 5 официантов (независимо от пола).
Сформировать все возможные варианты заполнения вакантных мест, если имеются 5 женщин и 5 мужчин.
"""
import itertools
import math
import time


def perf_func(func, *args) -> float:
    """
    Функция для вычисления времени выполнения функции.

    :param func: функция
    :param args: аргументы функции
    :return: время выполнения функции в наносекундах
    """

    start = time.perf_counter_ns()
    func(*args)
    end = time.perf_counter_ns()
    return end - start


def combination(n: int, k: int) -> int:
    """
    Вычисляет количество способов выбрать k элементов из n элементов без повторений.
    Вычисляет значение n! / (k! * (n - k)!), когда k <= n, и равно нулю, когда k > n.

    :param n: целое положительное число
    :param k: целое положительное число
    :return: сочетания из n по k без повторений
    """

    if n < 0 or k < 0:
        raise ValueError("Значения n и k должны быть положительными числами")

    if k > n:
        return 0

    if k == n:
        return 1

    if n - k == 1:
        return n

    return math.factorial(n) // (math.factorial(k) * math.factorial(n - k))


def generate_combinations_algo(vacancies, candidates) -> int:
    """
    Функция для генерации всех возможных вариантов заполнения вакантных мест, алгоритмическим методом.

    :param vacancies: список вакансий
    :param candidates: список кандидатов
    :return: количество возможных вариантов заполнения вакантных мест
    """

    total_combinations = 0

    for vacancy in vacancies:
        vacancy_sex = vacancy['sex']
        vacancy_count = vacancy['count']
        filtered_candidates = []

        for candidate in candidates:
            if candidate['sex'] == vacancy_sex:
                filtered_candidates.append(candidate)
            elif vacancy_sex is None:
                filtered_candidates.append(candidate)

        if not filtered_candidates:
            continue

        current_combinations = combination(len(filtered_candidates), vacancy_count)

        if total_combinations and current_combinations:
            total_combinations = total_combinations * current_combinations
        elif not total_combinations and current_combinations:
            total_combinations = current_combinations

        candidates = [c for c in candidates if c not in filtered_candidates[:vacancy_count]]

    return total_combinations


def generate_combinations_algo_2(vacancies, candidates) -> int:
    """
    Усложненная функция для генерации всех возможных вариантов заполнения вакантных мест, алгоритмическим методом.

    :param vacancies: список вакансий
    :param candidates: список кандидатов
    :return: количество возможных вариантов заполнения вакантных мест
    """

    total_combinations = 0

    for vacancy in vacancies:
        vacancy_sex = vacancy['sex']
        vacancy_exp = vacancy['exp']
        vacancy_role = vacancy['role']
        vacancy_count = vacancy['count']
        filtered_candidates = []

        for candidate in candidates:
            candidate_sex = candidate['sex']
            candidate_exp = candidate['exp']
            candidate_role = candidate['role']
            if candidate_sex == vacancy_sex and candidate_exp >= vacancy_exp and candidate_role == vacancy_role:
                filtered_candidates.append(candidate)
            elif vacancy_sex is None:
                filtered_candidates.append(candidate)

        if not filtered_candidates:
            continue

        current_combinations = combination(len(filtered_candidates), vacancy_count)

        if total_combinations and current_combinations:
            total_combinations = total_combinations * current_combinations
        elif not total_combinations and current_combinations:
            total_combinations = current_combinations

        candidates = [c for c in candidates if c not in filtered_candidates[:vacancy_count]]

    return total_combinations


def generate_combinations_funcs(vacancies, candidates) -> int:
    """
    Функция для генерации всех возможных вариантов заполнения вакантных мест, функциональным методом.

    :param vacancies: список вакансий
    :param candidates: список кандидатов
    :return: количество возможных вариантов заполнения вакантных мест
    """

    all_combinations = []

    for vacancy in vacancies:
        vacancy_sex = vacancy['sex']
        vacancy_count = vacancy['count']
        filtered_candidates = []

        for candidate in candidates:
            if candidate['sex'] == vacancy_sex:
                filtered_candidates.append(candidate)
            elif vacancy_sex is None:
                filtered_candidates.append(candidate)

        if not filtered_candidates:
            continue

        current_combinations = list(itertools.combinations(filtered_candidates, vacancy_count))

        if all_combinations and current_combinations:
            all_combinations = list(itertools.product(all_combinations, current_combinations))
        elif not all_combinations and current_combinations:
            all_combinations = current_combinations

        candidates = [c for c in candidates if c not in filtered_candidates[:vacancy_count]]

    return len(all_combinations)


def generate_combinations_funcs_2(vacancies, candidates) -> int:
    """
    Усложненная функция для генерации всех возможных вариантов заполнения вакантных мест, функциональным методом.

    :param vacancies: список вакансий
    :param candidates: список кандидатов
    :return: количество возможных вариантов заполнения вакантных мест
    """
    all_combinations = []

    for vacancy in vacancies:
        vacancy_sex = vacancy['sex']
        vacancy_exp = vacancy['exp']
        vacancy_role = vacancy['role']
        vacancy_count = vacancy['count']
        filtered_candidates = []

        for candidate in candidates:
            candidate_sex = candidate['sex']
            candidate_exp = candidate['exp']
            candidate_role = candidate['role']
            if candidate_sex == vacancy_sex and candidate_exp >= vacancy_exp and candidate_role == vacancy_role:
                filtered_candidates.append(candidate)
            elif vacancy_sex is None:
                filtered_candidates.append(candidate)

        if not filtered_candidates:
            continue

        current_combinations = list(itertools.combinations(filtered_candidates, vacancy_count))

        if all_combinations and current_combinations:
            all_combinations = list(itertools.product(all_combinations, current_combinations))
        elif not all_combinations and current_combinations:
            all_combinations = current_combinations

        candidates = [c for c in candidates if c not in filtered_candidates[:vacancy_count]]

    return len(all_combinations)


def solution_1():
    vacancies = [
        {'role': 'посудомойка', 'sex': 'женщина', 'count': 2},
        {'role': 'грузчик', 'sex': 'мужчина', 'count': 5},
        {'role': 'официант', 'sex': None, 'count': 5},
    ]

    candidates = [
        {'id': 1, 'sex': 'женщина'},
        {'id': 2, 'sex': 'женщина'},
        {'id': 3, 'sex': 'женщина'},
        {'id': 4, 'sex': 'женщина'},
        {'id': 5, 'sex': 'женщина'},

        {'id': 6, 'sex': 'мужчина'},
        {'id': 7, 'sex': 'мужчина'},
        {'id': 8, 'sex': 'мужчина'},
        {'id': 9, 'sex': 'мужчина'},
        {'id': 10, 'sex': 'мужчина'},
        {'id': 11, 'sex': 'мужчина'},
        {'id': 12, 'sex': 'мужчина'},
        {'id': 13, 'sex': 'мужчина'},
        {'id': 14, 'sex': 'мужчина'},
        {'id': 15, 'sex': 'мужчина'},
    ]

    print(f"Кафе набирает сотрудников: {vacancies[0]['count']} посудомойки (женщины), {vacancies[1]['count']} грузчиков (мужчины), {vacancies[2]['count']} официантов (независимо от пола).")
    print(f"Сформировать все возможные варианты заполнения вакантных мест, если имеются {len([c for c in candidates if c['sex'] == 'женщина'])} женщин и {len([c for c in candidates if c['sex'] == 'мужчина'])} мужчин.")

    print(f'\nАлгоритмический способ:')
    print(f'Количество вариантов заполнения вакантных мест: {generate_combinations_algo(vacancies, candidates)}')
    print(f'Время выполнения (наносек): {perf_func(generate_combinations_algo, vacancies, candidates)}')

    print(f'\nФункциональный способ:')
    print(f'Количество вариантов заполнения вакантных мест: {generate_combinations_funcs(vacancies, candidates)}')
    print(f'Время выполнения (наносек): {perf_func(generate_combinations_funcs, vacancies, candidates)}')


def solution_2():
    vacancies = [
        {'role': 'посудомойка', 'sex': 'женщина', 'exp': 1, 'count': 2},
        {'role': 'грузчик', 'sex': 'мужчина', 'exp': 3, 'count': 5},
        {'role': 'официант', 'sex': None, 'exp': 4, 'count': 5},
    ]

    candidates = [
        {'id': 1, 'sex': 'женщина', 'role': 'посудомойка', 'exp': 1},
        {'id': 2, 'sex': 'женщина', 'role': 'посудомойка', 'exp': 2},
        {'id': 3, 'sex': 'женщина', 'role': 'посудомойка', 'exp': 3},
        {'id': 4, 'sex': 'женщина', 'role': 'посудомойка', 'exp': 4},
        {'id': 5, 'sex': 'женщина', 'role': 'посудомойка', 'exp': 5},
        {'id': 6, 'sex': 'мужчина', 'role': 'грузчик', 'exp': 1},
        {'id': 7, 'sex': 'мужчина', 'role': 'грузчик', 'exp': 2},
        {'id': 8, 'sex': 'мужчина', 'role': 'грузчик', 'exp': 3},
        {'id': 9, 'sex': 'мужчина', 'role': 'грузчик', 'exp': 4},
        {'id': 10, 'sex': 'мужчина', 'role': 'грузчик', 'exp': 5},
        {'id': 11, 'sex': 'мужчина', 'role': 'официант', 'exp': 1},
        {'id': 12, 'sex': 'мужчина', 'role': 'официант', 'exp': 2},
        {'id': 13, 'sex': 'мужчина', 'role': 'официант', 'exp': 3},
        {'id': 14, 'sex': 'мужчина', 'role': 'официант', 'exp': 4},
        {'id': 15, 'sex': 'мужчина', 'role': 'официант', 'exp': 5},
    ]

    print("\n\nУсложенный вариант с добавлением ограничений характеристик (специальность, пол и стаж работы)")

    print(f'\nАлгоритмический способ:')
    print(f'Количество вариантов заполнения вакантных мест: {generate_combinations_algo_2(vacancies, candidates)}')
    print(f'Время выполнения (наносек): {perf_func(generate_combinations_algo_2, vacancies, candidates)}')

    print(f'\nФункциональный способ:')
    print(f'Количество вариантов заполнения вакантных мест: {generate_combinations_funcs_2(vacancies, candidates)}')
    print(f'Время выполнения (наносек): {perf_func(generate_combinations_funcs_2, vacancies, candidates)}')


def main():
    solution_1()
    solution_2()


if __name__ == '__main__':
    main()
