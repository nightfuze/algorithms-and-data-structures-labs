import secrets
from typing import List

COLS_NOT_EQUAL_ROWS = "Количество столбцов в первой матрице должно быть равно количеству строк во второй"

INVALID_SIZE_MATRICES = "Размер матриц не совпадает"
ERROR_EMPTY_LIST_MATRICES = "Пустой список матриц"

INVALID_INSTANCE_OF_MATRIX = "Матрица не является экземпляром класса"
INVALID_INSTANCE_OF_MATRICES = "Все матрицы в списке должны быть экземляром класса Matrix"


class Matrix:
    def __init__(self, rows, cols):
        self._data = []
        self.rows = rows
        self.cols = cols
        self._fill_zeroes()

    @classmethod
    def from_matrices(cls, matrices: List[List['Matrix']]) -> 'Matrix':
        if not matrices:
            raise ValueError(ERROR_EMPTY_LIST_MATRICES)

        block_rows = len(matrices)
        block_cols = len(matrices[0])

        matrix = matrices[0][0]

        for block_row in range(block_rows):
            for block_col in range(block_cols):
                if not isinstance(matrices[block_row][block_col], Matrix):
                    raise TypeError(INVALID_INSTANCE_OF_MATRICES)
                if (matrices[block_row][block_col].rows != matrix.rows or
                        matrices[block_row][block_col].cols != matrix.cols):
                    raise ValueError(INVALID_SIZE_MATRICES)

        new_rows = matrix.rows * block_rows
        new_cols = matrix.cols * block_cols
        new_matrix = cls(new_rows, new_cols)

        for block_row in range(block_rows):
            for block_col in range(block_cols):
                for row in range(matrix.rows):
                    for col in range(matrix.cols):
                        new_matrix[block_row * matrix.rows + row][block_col * matrix.cols + col] = \
                            matrices[block_row][block_col][row][col]

        return new_matrix

    def __str__(self):
        return self._get_string()

    def __repr__(self):
        return str(self._data)

    def __len__(self):
        return len(self._data)

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def __add__(self, other):
        if not isinstance(other, Matrix):
            raise TypeError(INVALID_INSTANCE_OF_MATRIX)

        if not (self.rows == other.rows and self.cols == other.cols):
            raise ValueError(INVALID_SIZE_MATRICES)

        new_matrix = Matrix(self.rows, self.cols)

        for row in range(other.rows):
            for col in range(other.cols):
                new_matrix[row][col] = self[row][col] + other[row][col]

        return new_matrix

    def __sub__(self, other):
        return self.__add__(other.__mul__(-1))

    def __mul__(self, left_operand):
        if isinstance(left_operand, Matrix):
            if not (self.cols == left_operand.rows):
                raise ValueError(COLS_NOT_EQUAL_ROWS)

            new_matrix = Matrix(left_operand.rows, self.cols)

            for row in range(self.rows):
                for other_col in range(left_operand.cols):
                    for col in range(self.cols):
                        new_matrix[row][other_col] += self[row][col] * left_operand[col][other_col]

            return new_matrix

        if isinstance(left_operand, (int, float)):
            new_matrix = Matrix(self.rows, self.cols)

            for row in range(self.rows):
                for col in range(self.cols):
                    new_matrix[row][col] = self[row][col] * left_operand

            return new_matrix

        raise TypeError(INVALID_INSTANCE_OF_MATRIX)

    def __rmul__(self, right_operand):
        return self.__mul__(right_operand)

    def transpose(self):
        new_matrix = Matrix(self.cols, self.rows)

        for row in range(self.rows):
            for col in range(self.cols):
                new_matrix[col][row] = self[row][col]

        return new_matrix

    def is_symmetric_by_main_diagonal(self) -> bool:
        if self.rows != self.cols:
            return False

        size = self.rows

        for row in range(size):
            for col in range(size):
                if self[row][col] != self[col][row]:
                    return False

        return True

    def is_symmetric_by_secondary_diagonal(self) -> bool:
        if self.rows != self.cols:
            return False

        size = self.rows

        for row in range(size):
            for col in range(size):
                if self[row][col] != self[size - col - 1][size - row - 1]:
                    return False

        return True

    def swap_areas(self):
        n = self.rows
        for i in range(n // 2):
            for j in range(i + 1, n // 2):
                self[i][j], self[n - i - 1][j] = self[n - i - 1][j], self[i][j]

        for i in range(n // 2):
            for j in range(n // 2, n - i - 1):
                self[i][j], self[n - i - 1][j] = self[n - i - 1][j], self[i][j]

    def _fill_zeroes(self):
        self._data = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

    def _get_string(self) -> str:
        max_len: int = 0
        for row in range(self.rows):
            for cow in range(self.cols):
                len_element: int = len(str(self[row][cow]))
                if len_element > max_len:
                    max_len = len_element

        string_matrix = '\n'.join([' '.join(['%*d' % (max_len, el) for el in row]) for row in self._data])

        return string_matrix

    def fill_random(self, min_value: int = -10, max_value: int = 10):
        for row in range(self.rows):
            for col in range(self.cols):
                self[row][col] = secrets.randbelow(max_value + 1) + min_value

        return self

    def fill_value(self, num: int):
        for row in range(self.rows):
            for col in range(self.cols):
                self[row][col] = num
        return self
