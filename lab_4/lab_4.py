import matplotlib.pyplot as plt
import numpy as np


def get_input(text: str) -> int:
    while True:
        try:
            value = int(input(text))
            return value
        except ValueError:
            print("Ошибка: Значение должно быть целым числом. Попробуйте еще раз.")


def get_size(text: str) -> int:
    while True:
        try:
            value = get_input(text)
            if value < 6:
                raise ValueError
            return value
        except ValueError:
            print("Ошибка: Значение должно быть больше или равно 6. Попробуйте еще раз.")


def swap_areas(mat: np.ndarray, n: int) -> None:
    for i in range(n // 2):
        for j in range(i + 1, n // 2):
            mat[i][j], mat[n - i - 1][j] = mat[n - i - 1][j], mat[i][j]

    for i in range(n // 2):
        for j in range(n // 2, n - i - 1):
            mat[i][j], mat[n - i - 1][j] = mat[n - i - 1][j], mat[i][j]


def is_sym_by_main(mat: np.ndarray) -> bool:
    return np.all(mat.transpose() == mat)


def is_sym_by_secondary(mat: np.ndarray) -> bool:
    return is_sym_by_main(np.fliplr(mat))


def random_matrix(rows: int, cols: int) -> np.matrix:
    return np.matrix(np.random.randint(-10, 11, size=(rows, cols)))


def swap_sym(mat: np.ndarray, mid: int) -> None:
    mat[:mid, :mid], mat[mid:, :mid] = np.flipud(mat[mid:, :mid].copy()), np.flipud(mat[:mid, :mid].copy())


def swap_asym(mat: np.ndarray, mid: int) -> None:
    mat[mid:, :mid], mat[mid:, mid:] = mat[mid:, mid:].copy(), mat[mid:, :mid].copy()


def plot_matrix(mat, title) -> None:
    plt.imshow(mat)
    plt.title(title)
    plt.colorbar()
    plt.show()


def print_matrix(mat, title: str) -> None:
    print(title)
    print(mat)
    print()


def test():
    k = 2
    n = 6
    mid = n // 2
    a_lst = [
        [0, 9, 8, 7, 5, 6],
        [1, 2, 3, 4, 5, 5],
        [7, 6, 5, 4, 4, 7],
        [8, 4, 3, 5, 3, 8],
        [5, 2, 4, 6, 2, 9],
        [1, 5, 8, 7, 1, 0],
    ]
    a = np.matrix(np.asarray(a_lst))

    b = a[:mid, :mid]
    c = a[:mid, mid:]
    d = a[mid:, :mid]
    e = a[mid:, mid:]

    print_matrix(a, "A before")
    swap_sym(a, mid)
    # swap_asym(a, mid)

    print_matrix(b, "b")
    print_matrix(c, "c")
    print_matrix(d, "d")
    print_matrix(e, "e")

    print_matrix(a, "A after")
    # run(a, n, k)


def run(a: np.matrix, n: int, k: int):
    mid = n // 2

    print_matrix(a, "Матрица А")

    f = np.copy(a)
    print_matrix(a, "Матрица F")

    b = f[:mid, :mid]
    c = f[:mid, mid:]
    d = f[mid:, :mid]
    e = f[mid:, mid:]

    print_matrix(b, "Подматрица B")
    print_matrix(c, "Подматрица C")
    print_matrix(d, "Подматрица D")
    print_matrix(e, "Подматрица E")

    if is_sym_by_secondary(a):
        print("\nМатрица A симметрична относительно побочной диагонали")
        print("Замена местами симметрично В и D")
        swap_sym(f, mid)

    else:
        print("\nМатрица A не симметрична относительно побочной диагонали")
        print("Замена местами D и Е несимметрично")
        swap_asym(f, mid)

    print_matrix(f, "Матрица F")

    if np.linalg.det(a) > a.diagonal().sum() + np.fliplr(a).diagonal().sum():
        print("\nОпределитель матрицы А больше суммы диагональных элементов матрицы F")
        result = np.linalg.inv(a) * a.transpose() - k * np.linalg.inv(f)
        print_matrix(result, "A^(-1)*A^T – K * F^(-1)")
    else:
        print("\nОпределитель матрицы А меньше суммы диагональных элементов матрицы F")
        g = np.tril(a)
        print_matrix(g, "Нижняя треугольная матрица G")
        result = (a.transpose() + g - f.transpose()) * k
        print_matrix(result, "(A^Т + G - F^Т) * K")

    plot_matrix(f, "Матрица F")
    plot_matrix(b, "Подматрица B")
    plot_matrix(c, "Подматрица C")
    plot_matrix(d, "Подматрица D")
    plot_matrix(e, "Подматрица E")


def main():
    k = get_input("K = ")
    n = get_size("N = ")
    a = random_matrix(n, n)
    run(a, n, k)


if __name__ == '__main__':
    main()
    # test()
