# Требуется для своего варианта второй части л.р. №6 (усложненной программы) разработать реализацию
# с использованием графического интерфейса.
# Допускается использовать любую графическую библиотеку питона.
# Рекомендуется использовать внутреннюю библиотеку питона  tkinter.
# В программе должны быть реализованы минимум одно окно ввода, одно окно вывода (со скролингом),
# одно текстовое поле, одна кнопка.

import itertools
import time
import tkinter as tk
from dataclasses import dataclass, fields
from random import choice, randint
from tkinter import ttk
from typing import List, Tuple, Dict, Union

data_map: Dict[str, str] = {
    'id': 'Номер',
    'role': 'Специальность',
    'sex': 'Пол',
    'exp': 'Стаж работы',
    'count': 'Количество мест',
}


@dataclass
class BaseData:
    id: int

    @classmethod
    def keys(cls):
        return tuple(field.name for field in fields(cls))

    def values(self):
        return tuple(getattr(self, key) for key in self.keys())

    @classmethod
    def mapped_keys(cls):
        return tuple(data_map.get(key) for key in cls.keys())


@dataclass
class Vacancy(BaseData):
    role: str
    sex: Union[str, None]
    exp: int
    count: int


@dataclass
class Candidate(BaseData):
    sex: str
    exp: int


@dataclass
class OptimalCandidate(Candidate):
    role: str


class RecruitmentService:
    def __init__(self):
        self.total: int = 0
        self.optimal_combinations: Dict[str, List[Candidate]] = {}

        self.vacancies: List[Vacancy] = []
        self.candidates: List[Candidate] = []
        self.optimal_candidates: List[OptimalCandidate] = []
        self.time_elapsed = 0

    def __init_vacancies(self):
        self.vacancies = [
            Vacancy(1, 'посудомойка', 'женщина', 1, 2),
            Vacancy(2, 'грузчик', 'мужчина', 3, 5),
            Vacancy(3, 'официант', None, 1, 5),
        ]

    def __init_candidates(self):
        self.candidates = [
            Candidate(1, 'женщина', 1),
            Candidate(2, 'женщина', 2),
            Candidate(3, 'женщина', 3),
            Candidate(4, 'женщина', 4),
            Candidate(5, 'женщина', 5),
            Candidate(6, 'мужчина', 1),
            Candidate(7, 'мужчина', 2),
            Candidate(8, 'мужчина', 3),
            Candidate(9, 'мужчина', 4),
            Candidate(10, 'мужчина', 5),
            Candidate(11, 'мужчина', 1),
            Candidate(12, 'мужчина', 2),
            Candidate(13, 'мужчина', 3),
            Candidate(14, 'мужчина', 4),
            Candidate(15, 'мужчина', 5),
        ]

    def init_random_candidates(self, count: int):
        self.candidates = [Candidate(i, choice(['мужчина', 'женщина']), randint(1, 5)) for i in
                           range(1, abs(count) + 1)]

    def init_data(self):
        self.__init_vacancies()
        self.__init_candidates()

    @staticmethod
    def get_mapped_values(lst: List[Union[Vacancy, Candidate]]):
        return [item.values() for item in lst]

    def get_candidates_values(self) -> List[Tuple[Vacancy, ...]]:
        """
        Метод для получения списка значений полей кандидатов.
        """
        return self.get_mapped_values(self.candidates)

    def get_vacancies_values(self) -> List[Tuple[Vacancy, ...]]:
        """
        Метод для получения списка значений полей вакантных мест.
        """
        return self.get_mapped_values(self.vacancies)

    def get_optimal_candidates_values(self) -> List[Tuple[OptimalCandidate, ...]]:
        """
        Метод для получения списка значений полей оптимальных кандидатов.
        """
        return self.get_mapped_values(self.optimal_candidates)

    def generate_combinations(self) -> None:
        """
        Метод для генерации всех возможных вариантов заполнения вакантных мест.
        """
        start = time.perf_counter()
        all_combinations = []
        self.optimal_combinations: Dict[str, Tuple[Candidate]] = {}
        candidates = self.candidates

        for vacancy in self.vacancies:
            filtered_candidates = []

            for candidate in candidates:
                if candidate.sex == vacancy.sex and candidate.exp >= vacancy.exp:
                    filtered_candidates.append(candidate)
                elif vacancy.sex is None and candidate.exp >= vacancy.exp:
                    filtered_candidates.append(candidate)

            if not filtered_candidates:
                continue

            current_combinations: List[Tuple[Candidate]] = list(
                itertools.combinations(filtered_candidates, vacancy.count))

            if not current_combinations:
                continue

            self.optimal_combinations.update({vacancy.role: self.__find_optimal_combination(current_combinations)})

            if all_combinations:
                all_combinations = itertools.product(all_combinations, current_combinations)
                self.total *= len(current_combinations)
            elif not all_combinations:
                all_combinations = current_combinations
                self.total = len(current_combinations)

            lst_ids = [c.id for c in self.optimal_combinations[vacancy.role]]
            candidates = [c for c in candidates if c.id not in lst_ids]

        self.optimal_candidates = []
        for key, value in self.optimal_combinations.items():
            self.optimal_candidates.extend([OptimalCandidate(*c.values(), role=key) for c in value])

        end = time.perf_counter()
        self.time_elapsed = end - start

    @staticmethod
    def __find_optimal_combination(
            combination: List[Tuple[Candidate]],
    ) -> Tuple[Candidate]:
        """
        Метод для нахождения оптимального решения заполнения вакантных мест.
        Вакатные места заполняются на каждую вакансию, по сумме максимальноого стажа работы.

        :param combination: список вариантов заполнения вакантных мест
        :return: оптимальное заполнение вакантного места
        """

        optimal_combination = combination[0]
        optimal_comb_sum = sum(c.exp for c in optimal_combination)

        for curr_comb in combination:
            curr_comb_sum = sum(c.exp for c in curr_comb)

            if curr_comb_sum > optimal_comb_sum:
                optimal_combination = curr_comb
                optimal_comb_sum = curr_comb_sum

        return optimal_combination


class TableFrame(ttk.Frame):
    def __init__(self, parent, cols, display_cols, rows):
        super().__init__(parent)

        self.cols = cols
        self.display_cols = display_cols
        self.rows = rows

        self.table = ttk.Treeview(self, columns=self.cols, show='headings')

        for col, display_col in zip(self.cols, self.display_cols):
            self.table.heading(col, text=display_col)
            self.table.column(col, anchor=tk.CENTER)

        for row in self.rows:
            self.table.insert('', tk.END, values=row)

        self.scrolltable = ttk.Scrollbar(self, command=self.table.yview)
        self.table.configure(yscrollcommand=self.scrolltable.set)
        self.scrolltable.pack(side=tk.RIGHT, fill=tk.Y)
        self.table.pack()

    def update_all_records(self, rows):
        for i in self.table.get_children():
            self.table.delete(i)

        self.rows = rows
        for row in self.rows:
            self.table.insert('', tk.END, values=row)


class App(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.recruitment_service = RecruitmentService()

        button_mock_data = ttk.Button(self, text="Загрузить тестовые данные", command=self.init_data)
        button_mock_data.pack()

        label_frame_vacancy = ttk.Labelframe(self, text='Вакансии')
        label_frame_vacancy.pack(expand=True, fill=tk.BOTH)

        self.vacancy_table = TableFrame(label_frame_vacancy, Vacancy.keys(), Vacancy.mapped_keys(),
                                        self.recruitment_service.get_vacancies_values())
        self.vacancy_table.configure(padding=10)
        self.vacancy_table.pack()

        label_frame_candidate = ttk.LabelFrame(self, text='Кандидаты')
        label_frame_candidate.pack(expand=True, fill=tk.BOTH)

        self.text_total_generate = tk.StringVar()
        self.text_total_generate.set('10')
        entry_generate_candidates = ttk.Spinbox(label_frame_candidate, textvariable=self.text_total_generate)
        entry_generate_candidates.pack()

        button_generate_candidates = ttk.Button(label_frame_candidate, text='Сгенерировать кандидатов',
                                                command=self.generate_candidates)
        button_generate_candidates.pack()

        self.candidate_table = TableFrame(label_frame_candidate, Candidate.keys(), Candidate.mapped_keys(),
                                          self.recruitment_service.get_candidates_values())
        self.candidate_table.configure(padding=10)
        self.candidate_table.pack()

        label_frame_optimal_combination = ttk.LabelFrame(self, text='Оптимальный вариант')
        label_frame_optimal_combination.pack(expand=True, fill=tk.BOTH)

        button_generate = ttk.Button(label_frame_optimal_combination, text='Сгенерировать',
                                     command=self.generate_combinations)
        button_generate.pack()

        self.total_combinations_label = ttk.Label(label_frame_optimal_combination,
                                                  text=f'Всего вариантов: {self.recruitment_service.total}')
        self.total_combinations_label.pack()

        self.time_elapsed_label = ttk.Label(label_frame_optimal_combination,
                                            text=f'Время выполнения: {self.recruitment_service.time_elapsed}')
        self.time_elapsed_label.pack()

        self.optimal_table = TableFrame(label_frame_optimal_combination, OptimalCandidate.keys(),
                                        OptimalCandidate.mapped_keys(), [])
        self.optimal_table.configure(padding=10)
        self.optimal_table.pack()

    def init_data(self):
        self.recruitment_service.init_data()
        self.vacancy_table.update_all_records(self.recruitment_service.get_vacancies_values())
        self.candidate_table.update_all_records(self.recruitment_service.get_candidates_values())

    def generate_combinations(self):
        self.recruitment_service.generate_combinations()
        self.total_combinations_label.config(text=f'Всего вариантов: {self.recruitment_service.total}')
        self.time_elapsed_label.config(text=f'Время выполнения: {self.recruitment_service.time_elapsed}')

        self.optimal_table.update_all_records(self.recruitment_service.get_optimal_candidates_values())

    def generate_candidates(self):
        self.recruitment_service.init_random_candidates(int(self.text_total_generate.get()))
        self.candidate_table.update_all_records(self.recruitment_service.get_candidates_values())


class Window(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Набор сотрудников в Кафе')

        self.app = App(self)
        self.app.configure(padding=30)
        self.app.pack()


def main():
    window = Window()
    window.mainloop()


if __name__ == '__main__':
    main()
