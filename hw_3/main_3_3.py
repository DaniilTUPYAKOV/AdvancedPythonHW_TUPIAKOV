import numpy as np


class HashMixin:

    def __hash__(self) -> int:
        my_hash = 0
        for elem in str(self):
            my_hash += ord(elem)
        return my_hash


class Matrix(HashMixin):
    
    __chache = {}

    def __init__(self, matrix):
        if not isinstance(matrix, list):
            raise TypeError("Expected argument '_matrix' to be a list")
        if len(matrix) == 0:
            raise ValueError("All rows in '_matrix' must have the same length")
        for elem in matrix:
            if len(elem) != len(matrix[0]):
                raise ValueError(
                    "All rows in '_matrix' must have the same length")
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
            [self._matrix[i][j] + other._matrix[i][j]
                for j in range(self._cols_num)]
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
            [self._matrix[i][k] * other._matrix[i][k]
                for k in range(self._cols_num)]
            for i in range(self._rows_num)
        ]
        return Matrix(result)

    @check_arg_type
    def __matmul__(self, other: "Matrix"):

        chache = hash(self) * 4 * hash(other)
        if chache in self.__chache:
            return Matrix(self.__chache[chache])

        if self._cols_num != other._rows_num or self._rows_num != other._cols_num:
            raise ValueError("Matrices cannot be multiplied.")

        result = [
            [sum(a * b for a, b in zip(A_row, B_col))
             for B_col in zip(*other._matrix)]
            for A_row in self._matrix
        ]

        self.__chache[chache] = result
        return Matrix(result)

    def __str__(self) -> str:
        return "\n".join([" ".join([str(elem) for elem in row]) for row in self._matrix])


np.random.seed(0)
A = Matrix(np.random.randint(0, 10, (10, 10)).tolist())
C = Matrix(np.array(A._matrix).transpose().tolist())

B = Matrix(np.random.randint(0, 10, (10, 10)).tolist())
D = B

if ((hash(A) == hash(C)) and (A != C) and (B == D) and (A @ B != C @ D)):

    AB = A @ B
    CD = C @ D

    def save_result_mat(mat: Matrix, filename: str):
        with open(filename, "w", encoding="utf-8") as file:
            file.write("\n".join([" ".join(map(str, row)) for row in mat._matrix]))

    def save_result_text(text: str, prefix: str, filename: str):
        with open(filename, "+a", encoding="utf-8") as file:
            file.write(prefix + " " + text + "\n")


    save_result_mat(A, "A.txt")
    save_result_mat(B, "B.txt")
    save_result_mat(C, "C.txt")
    save_result_mat(D, "D.txt")
    save_result_mat(AB, "AB.txt")
    # save_result_mat(CD, "CD.txt")
    save_result_text(str(hash(AB)), "Hash AB =", "hash.txt")
    save_result_text(str(hash(CD)), "Hash CD =", "hash.txt")
