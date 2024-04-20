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
import time
from typing import Tuple, Optional, Any, List


def perf_func(func, *args) -> Tuple[int, Any]:
    """
    Функция для вычисления времени выполнения функции.

    :param func: функция
    :param args: аргументы функции
    :return: кортеж (время выполнения функции в наносекундах, результат функции)
    """

    start = time.perf_counter_ns()
    result = func(*args)
    end = time.perf_counter_ns()
    return end - start, result


def combinations(iterable: List[Any], r: Optional[int] = None) -> List[tuple]:
    """
    Фукнция для генерации сочетаний элементов списка длины r.
    :param iterable: список элементов
    :param r: количество элементов в сочетании
    :return: список сочетаний
    """

    pool = tuple(iterable)
    n = len(pool)
    r = n if r is None else r

    if r > n:
        return []

    indices = list(range(r))
    result = [tuple(pool[i] for i in indices)]
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            break
        indices[i] += 1
        for j in range(i + 1, r):
            indices[j] = indices[j - 1] + 1
        result.append(tuple(pool[i] for i in indices))
    return result


def product(*args, repeat=1) -> List[tuple]:
    """
    Функция для генерации всех возможных комбинации элементов из переданных аргументов.

    :param args: Итерируемые объекты, элементы которых будут использоваться для генерации комбинаций.
    :param repeat: Количество повторений каждого аргумента в комбинациях. По умолчанию равно 1.
    :return: Список кортежей, который представляют собой все возможные комбинации.
    """

    pools = [tuple(pool) for pool in args] * repeat
    result = [[]]
    for pool in pools:
        result = [x + [y] for x in result for y in pool]
    return [tuple(prod) for prod in result]


def find_optimal_combination(combination, optimal_combinations, vacancy_count, vacancy_role):
    """
    Целевая функция для нахождения оптимального решения заполнения вакантных мест.

    :param combination: список вариантов заполнения вакантных мест
    :param optimal_combinations: оптимальный список вариантов заполнения вакантных мест
    :param vacancy_count: количество вакантных мест
    :param vacancy_role: специальность вакантного места
    :return: оптимальное заполнение вакантных мест
    """

    for curr_comb in combination:
        curr_comb_sorted = sorted(curr_comb, key=lambda c: c['exp'], reverse=True)[:vacancy_count]
        if optimal_combinations.get(vacancy_role) is not None:
            optimal_comb_sorted = sorted(optimal_combinations[vacancy_role], key=lambda c: c['exp'], reverse=True)[
                                  :vacancy_count]
            optimal_comb_sum = sum([c['exp'] for c in optimal_comb_sorted])
            curr_comb_sum = sum([c['exp'] for c in curr_comb_sorted])

            if curr_comb_sum > optimal_comb_sum:
                optimal_combinations[vacancy_role] = curr_comb_sorted
        else:
            optimal_combinations[vacancy_role] = curr_comb_sorted

    return optimal_combinations


def generate_combinations_algo(vacancies, candidates) -> int:
    """
    Функция для генерации всех возможных вариантов заполнения вакантных мест, алгоритмическим методом.

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

        current_combinations = combinations(filtered_candidates, vacancy_count)

        if all_combinations and current_combinations:
            all_combinations = product(all_combinations, current_combinations)
        elif not all_combinations and current_combinations:
            all_combinations = current_combinations

        candidates = [c for c in candidates if c not in filtered_candidates[:vacancy_count]]

    return len(all_combinations)


def generate_combinations_algo_2(vacancies, candidates) -> Tuple[int, dict]:
    """
    Усложненная функция для генерации всех возможных вариантов заполнения вакантных мест, алгоритмическим методом.

    :param vacancies: список вакансий
    :param candidates: список кандидатов
    :return: количество возможных вариантов заполнения вакантных мест и оптимальный вариант заполнения вакантных мест
    """

    all_combinations = 0
    optimal_combinations = {}

    for vacancy in vacancies:
        vacancy_role = vacancy['role']
        vacancy_sex = vacancy['sex']
        vacancy_exp = vacancy['exp']
        vacancy_count = vacancy['count']
        filtered_candidates = []

        for candidate in candidates:
            candidate_sex = candidate['sex']
            candidate_exp = candidate['exp']
            if candidate_sex == vacancy_sex and candidate_exp >= vacancy_exp:
                filtered_candidates.append(candidate)
            elif vacancy_sex is None and candidate_exp >= vacancy_exp:
                filtered_candidates.append(candidate)

        if not filtered_candidates:
            continue

        current_combinations = combinations(filtered_candidates, vacancy_count)

        optimal_combinations = find_optimal_combination(current_combinations, optimal_combinations, vacancy_count,
                                                        vacancy_role)

        if all_combinations and current_combinations:
            all_combinations = product(all_combinations, current_combinations)
        elif not all_combinations and current_combinations:
            all_combinations = current_combinations

        candidates = [c for c in candidates if c not in filtered_candidates[:vacancy_count]]

    return len(all_combinations), optimal_combinations


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


def generate_combinations_funcs_2(vacancies, candidates) -> Tuple[int, dict]:
    """
    Усложненная функция для генерации всех возможных вариантов заполнения вакантных мест, функциональным методом.

    :param vacancies: список вакансий
    :param candidates: список кандидатов
    :return: количество возможных вариантов заполнения вакантных мест и оптимальный вариант заполнения вакантных мест
    """
    all_combinations = []
    optimal_combinations = {}

    for vacancy in vacancies:
        vacancy_role = vacancy['role']
        vacancy_sex = vacancy['sex']
        vacancy_exp = vacancy['exp']
        vacancy_count = vacancy['count']
        filtered_candidates = []

        for candidate in candidates:
            candidate_sex = candidate['sex']
            candidate_exp = candidate['exp']
            if candidate_sex == vacancy_sex and candidate_exp >= vacancy_exp:
                filtered_candidates.append(candidate)
            elif vacancy_sex is None and candidate_exp >= vacancy_exp:
                filtered_candidates.append(candidate)

        if not filtered_candidates:
            continue

        current_combinations = list(itertools.combinations(filtered_candidates, vacancy_count))

        optimal_combinations = find_optimal_combination(current_combinations, optimal_combinations, vacancy_count, vacancy_role)

        if all_combinations and current_combinations:
            all_combinations = list(itertools.product(all_combinations, current_combinations))
        elif not all_combinations and current_combinations:
            all_combinations = current_combinations

        candidates = [c for c in candidates if c not in filtered_candidates[:vacancy_count]]

    return len(all_combinations), optimal_combinations


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

    men = [len([c for c in candidates if c['sex'] == 'мужчина'])]
    women = [len([c for c in candidates if c['sex'] == 'женщина'])]

    dish_washers = [vacancies[0]['count']]
    loaders = [vacancies[1]['count']]
    waiters = [vacancies[2]['count']]

    print(f"Кафе набирает сотрудников: {dish_washers} посудомойки (женщины), {loaders} грузчиков (мужчины), {waiters} официантов (независимо от пола).")
    print(f"Сформировать все возможные варианты заполнения вакантных мест, если имеются {women} женщин и {men} мужчин.")

    time_algo, result_algo = perf_func(generate_combinations_algo, vacancies, candidates)
    time_func, result_funcs = perf_func(generate_combinations_funcs, vacancies, candidates)

    print(f'\nАлгоритмический способ:')
    print(f'Количество вариантов заполнения вакантных мест: {result_algo}')
    print(f'Время выполнения (наносек): {time_algo}')

    print(f'\nФункциональный способ:')
    print(f'Количество вариантов заполнения вакантных мест: {result_funcs}')
    print(f'Время выполнения (наносек): {time_func}')


def solution_2():
    vacancies = [
        {'role': 'посудомойка', 'sex': 'женщина', 'exp': 1, 'count': 2},
        {'role': 'грузчик', 'sex': 'мужчина', 'exp': 3, 'count': 5},
        {'role': 'официант', 'sex': None, 'exp': 1, 'count': 5},
    ]

    candidates = [
        {'id': 1, 'sex': 'женщина', 'exp': 1},
        {'id': 2, 'sex': 'женщина', 'exp': 2},
        {'id': 3, 'sex': 'женщина', 'exp': 3},
        {'id': 4, 'sex': 'женщина', 'exp': 4},
        {'id': 5, 'sex': 'женщина', 'exp': 5},
        {'id': 6, 'sex': 'мужчина', 'exp': 1},
        {'id': 7, 'sex': 'мужчина', 'exp': 2},
        {'id': 8, 'sex': 'мужчина', 'exp': 3},
        {'id': 9, 'sex': 'мужчина', 'exp': 4},
        {'id': 10, 'sex': 'мужчина', 'exp': 5},
        {'id': 11, 'sex': 'мужчина', 'exp': 1},
        {'id': 12, 'sex': 'мужчина', 'exp': 2},
        {'id': 13, 'sex': 'мужчина', 'exp': 3},
        {'id': 14, 'sex': 'мужчина', 'exp': 4},
        {'id': 15, 'sex': 'мужчина', 'exp': 5},
    ]

    print("\n\nУсложенный вариант с добавлением ограничений на характеристики (пол и стаж работы)")

    time_algo_2, result_algo_2 = perf_func(generate_combinations_algo_2, vacancies, candidates)
    time_func_2, result_func_2 = perf_func(generate_combinations_funcs_2, vacancies, candidates)

    print(f'\nАлгоритмический способ:')
    print(f'Количество вариантов заполнения вакантных мест: {result_algo_2[0]}')
    print(f'Оптимальный вариант заполнения вакантных мест: {result_algo_2[1]}')
    print(f'Время выполнения (наносек): {time_algo_2}')

    print(f'\nФункциональный способ:')
    print(f'Количество вариантов заполнения вакантных мест: {result_func_2[0]}')
    print(f'Оптимальный вариант заполнения вакантных мест: {result_func_2[1]}')
    print(f'Время выполнения (наносек): {time_func_2}')


def main():
    solution_1()
    solution_2()


if __name__ == '__main__':
    main()
