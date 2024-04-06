"""
Дана матрица.
Вывести значения элементов - пройтись змейкой (начиная с левого верхнего) вдоль главной диагонали.
"""

from typing import List, Union

Matrix = List[List[Union[float, int]]]


def print_traverse_matrix(mat: Matrix) -> None:
    rows, cols = len(mat), len(mat[0])
    row, col = 0, 0

    direction_up = True

    while row != rows and col != cols:
        if direction_up:
            while row >= 0 and col < cols:
                print(mat[row][col])
                if col == cols - 1:
                    direction_up = False
                    row += 1
                    break
                elif row == 0:
                    direction_up = False
                    col += 1
                    break
                row -= 1
                col += 1
        else:
            while row < rows and col < cols:
                print(mat[row][col])
                if row == rows - 1:
                    direction_up = True
                    col += 1
                    break
                elif col == 0:
                    direction_up = True
                    row += 1
                    break
                row += 1
                col -= 1


def main():
    matA = [
        [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7],
        [1.0, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7],
        [2.0, 2.1, 2.2, 2.3, 2.4, 2.5, 2.6, 2.7],
        [3.0, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 3.7],
        [4.0, 4.1, 4.2, 4.3, 4.4, 4.5, 4.6, 4.7],
        [5.0, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6, 5.7],
        [6.0, 6.1, 6.2, 6.3, 6.4, 6.5, 6.6, 6.7],
        [7.0, 7.1, 7.2, 7.3, 7.4, 7.5, 7.6, 7.7]
    ]

    matB = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 9]
    ]

    matC = [
        [1, 2, 3, 4],
        [5, 6, 7, 8],
        [9, 10, 11, 12],
        [13, 14, 15, 16],
        [17, 18, 19, 20]
    ]

    print_traverse_matrix(matA)
    print()
    print_traverse_matrix(matB)
    print()
    print_traverse_matrix(matC)


if __name__ == '__main__':
    main()
