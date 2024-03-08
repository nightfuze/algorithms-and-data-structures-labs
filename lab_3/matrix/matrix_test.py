import unittest

from matrix import Matrix


class TestMatrixMethods(unittest.TestCase):
    def test_matrix_addition(self):
        matrix1 = Matrix(2, 2)
        matrix1._data = [[1, 2], [3, 4]]

        matrix2 = Matrix(2, 2)
        matrix2._data = [[5, 6], [7, 8]]

        result_matrix = matrix1 + matrix2
        expected_result = [[6, 8], [10, 12]]

        self.assertEqual(expected_result, result_matrix._data)

    def test_matrix_addition_invalid_type(self):
        matrix1 = Matrix(2, 2)
        matrix2 = [[1, 2], [3, 4]]

        with self.assertRaises(TypeError):
            result_matrix = matrix1 + matrix2

    def test_matrix_addition_invalid_size(self):
        matrix1 = Matrix(2, 2)
        matrix1._data = [[1, 2], [3, 4]]

        matrix2 = Matrix(3, 3)
        matrix2._data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

        with self.assertRaises(ValueError):
            result_matrix = matrix1 + matrix2

    def test_matrix_subtraction(self):
        matrix1 = Matrix(2, 2)
        matrix1._data = [[1, 2], [3, 4]]

        matrix2 = Matrix(2, 2)
        matrix2._data = [[5, 6], [7, 8]]

        result_matrix = matrix1 - matrix2
        expected_result = [[-4, -4], [-4, -4]]

        self.assertEqual(expected_result, result_matrix._data)

    def test_matrix_subtraction_invalid_type(self):
        matrix1 = Matrix(2, 2)
        matrix2 = [[1, 2], [3, 4]]

        with self.assertRaises(TypeError):
            result_matrix = matrix1 - matrix2

    def test_matrix_subtraction_invalid_size(self):
        matrix1 = Matrix(2, 2)
        matrix1._data = [[1, 2], [3, 4]]

        matrix2 = Matrix(3, 3)
        matrix2._data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

        with self.assertRaises(ValueError):
            result_matrix = matrix1 - matrix2

    def test_matrix_multiplication(self):
        matrix1 = Matrix(3, 3)
        matrix1._data = [[-3, -7, 4], [1, 4, 9], [-9, 6, 7]]

        matrix2 = Matrix(3, 3)
        matrix2._data = [[-2, 5, -6], [-5, -3, 0], [2, -3, -6]]

        result_matrix = matrix1 * matrix2
        expected_result = [[49, -6, -6], [-4, -34, -60], [2, -84, 12]]

        self.assertEqual(expected_result, result_matrix._data)

    def test_matrix_scalar_multiplication(self):
        matrix = Matrix(3, 3)
        matrix._data = [[-2, 5, -6], [-5, -3, 0], [2, -3, -6]]

        result_matrix = matrix * 2
        expected_result = [[-4, 10, -12], [-10, -6, 0], [4, -6, -12]]

        self.assertEqual(expected_result, result_matrix._data)

    def test_transpose(self):
        matrix = Matrix(3, 2)
        matrix._data = [[1, 2], [3, 4], [5, 6]]

        transposed_matrix = matrix.transpose()
        expected_result = [[1, 3, 5], [2, 4, 6]]

        self.assertEqual(transposed_matrix.rows, matrix.cols)
        self.assertEqual(transposed_matrix.cols, matrix.rows)

        self.assertEqual(expected_result, transposed_matrix._data)

    def test_fill_random(self):
        size = 2
        matrix = Matrix(size, size)
        matrix.fill_random(-10, 10)

        self.assertEqual(len(matrix._data), size)
        self.assertEqual(len(matrix._data[0]), size)
        self.assertEqual(len(matrix._data[1]), size)

    def test_main_symmetric_true(self):
        size = 3
        matrix = Matrix(size, size)
        matrix._data = [
            [1, 2, 3],
            [2, 0, 4],
            [3, 4, 5]
        ]
        result = matrix.is_symmetric_by_main_diagonal()
        expected_result = True
        self.assertEqual(expected_result, result)

    def test_main_symmetric_false(self):
        size = 3
        matrix = Matrix(size, size)
        matrix._data = [
            [4, 1, 3],
            [6, 2, 1],
            [7, 6, 4]
        ]
        result = matrix.is_symmetric_by_main_diagonal()
        expected_result = False
        self.assertEqual(expected_result, result)

    def test_secondary_symmetric_true(self):
        size = 3
        matrix = Matrix(size, size)
        matrix._data = [
            [4, 1, 3],
            [6, 2, 1],
            [7, 6, 4]
        ]
        result = matrix.is_symmetric_by_secondary_diagonal()
        expected_result = True
        self.assertEqual(expected_result, result)

    def test_secondary_symmetric_false(self):
        size = 3
        matrix = Matrix(size, size)
        matrix._data = [
            [1, 2, 3],
            [2, 0, 4],
            [3, 4, 5]
        ]
        result = matrix.is_symmetric_by_secondary_diagonal()
        expected_result = False
        self.assertEqual(expected_result, result)


if __name__ == '__main__':
    unittest.main()
