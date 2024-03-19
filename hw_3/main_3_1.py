import numpy as np


class Matrix(np.lib.mixins.NDArrayOperatorsMixin):

    def __init__(self, matrix):
        if not isinstance(matrix, list):
            raise TypeError("Expected argument '_matrix' to be a list")
        if len(matrix) == 0:
            raise ValueError("All rows in '_matrix' must have the same length")
        for elem in matrix:
            if len(elem) != len(matrix[0]):
                raise ValueError("All rows in '_matrix' must have the same length")
        self._matrix = matrix
        self._rows_num = len(matrix)
        self._cols_num = len(matrix[0])

    @staticmethod
    def check_arg_type(function):
        def wrapper(*args, **kwargs):
            if not isinstance(args[0], Matrix):
                raise TypeError(
                    f"Operation undefined for type Mtrix and {type(args[0])}!"
                )
            return function(*args, **kwargs)

        return wrapper

    @check_arg_type
    def __add__(self, other: "Matrix"):
        if self._rows_num != other._rows_num or self._cols_num != other._cols_num:
            raise ValueError("Matrices are not the same size!")
        result = [
            [self._matrix[i][j] + other._matrix[i][j] for j in range(self._cols_num)]
            for i in range(self._rows_num)
        ]
        return Matrix(result)

    @check_arg_type
    def __mul__(self, other: "Matrix"):
        if self._cols_num != other._cols_num or self._rows_num != other._rows_num:
            raise ValueError(
                f"""Matrices have different shapes 
                    ({self._rows_num}, {self._cols_num}) 
                    and ({other._rows_num}, {other._cols_num}) 
                    so cannot be element-by-element multiplied!"""
            )
        result = [
            [self._matrix[i][k] * other._matrix[i][k] for k in range(self._cols_num)]
            for i in range(self._rows_num)
        ]
        return Matrix(result)

    @check_arg_type
    def __matmul__(self, other: "Matrix"):
        if self._cols_num != other._rows_num or self._rows_num != other._cols_num:
            raise ValueError("Matrices cannot be multiplied.")

        result = [
            [sum(a * b for a, b in zip(A_row, B_col)) for B_col in zip(*other._matrix)]
            for A_row in self._matrix
        ]

        return Matrix(result)


np.random.seed(0)
matrix_a = Matrix(np.random.randint(0, 10, (10, 10)).tolist())
matrix_b = Matrix(np.random.randint(0, 10, (10, 10)).tolist())


def save_result(mat: Matrix, filename: str):
    with open(filename, "w", encoding="utf-8") as file:
        file.write("\n".join([" ".join(map(str, row)) for row in mat]))


save_result(matrix_a, "matrix_a.txt")
save_result(matrix_b, "matrix_b.txt")
save_result(matrix_a + matrix_b, "matrix+.txt")
save_result(matrix_a * matrix_b, "matrix_mult.txt")
save_result(matrix_a @ matrix_b, "matrix@.txt")

print(
    (np.array(matrix_a.matrix) + np.array(matrix_b.matrix)).tolist()
    == (matrix_a + matrix_b).matrix
)
print(
    (np.array(matrix_a.matrix) * np.array(matrix_b.matrix)).tolist()
    == (matrix_a * matrix_b).matrix
)
print(
    (np.array(matrix_a.matrix) @ np.array(matrix_b.matrix)).tolist()
    == (matrix_a @ matrix_b).matrix
)
