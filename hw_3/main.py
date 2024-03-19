class Matrix:

    def __init__(self, matrix):
        if not isinstance(matrix, list):
            raise TypeError("Expected argument 'matrix' to be a list")
        if len(matrix) == 0:
            raise ValueError("All rows in 'matrix' must have the same length")
        for elem in matrix:
            if len(elem) != len(matrix[0]):
                raise ValueError("All rows in 'matrix' must have the same length")
        self._matrix = matrix
        self._rows_num = len(matrix)
        self._cols_num = len(matrix[0])

    @property
    def matrix(self):
        return self._matrix

    @property
    def rows_num(self):
        return self._rows_num

    @property
    def cols_num(self):
        return self._cols_num

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
        if self.rows_num != other.rows_num or self.cols_num != other.cols_num:
            raise ValueError("Matrices are not the same size!")
        result = [
            [self.matrix[i][j] + other.matrix[i][j] for j in range(self.cols_num)]
            for i in range(self.rows_num)
        ]
        return Matrix(result)

    @check_arg_type
    def __mul__(self, other: "Matrix"):
        if self.cols_num != other.cols_num or self.rows_num != other.rows_num:
            raise ValueError(
                f"""Matrices have different shapes 
                    ({self.rows_num}, {self.cols_num}) 
                    and ({other.rows_num}, {other.cols_num}) 
                    so cannot be element-by-element multiplied!"""
            )
        result = [
            [self.matrix[i][k] * other.matrix[i][k] for k in range(self.cols_num)]
            for i in range(self.rows_num)
        ]
        return Matrix(result)

    @check_arg_type
    def __matmul__(self, other: "Matrix"):
        if self.cols_num != other.rows_num or self.rows_num != other.cols_num:
            raise ValueError("Matrices cannot be multiplied.")

        result = [
            [sum(a * b for a, b in zip(A_row, B_col)) for B_col in zip(*self.matrix)]
            for A_row in other.matrix
        ]

        return Matrix(result)

    def __str__(self):
        return "\n".join([" ".join(map(str, row)) for row in self.matrix])


# Example usage:
# Create two matrix instances
m1 = Matrix([[1, 2, 1], [3, 4, 2]])
m2 = Matrix([[5, 6], [7, 8]])

# Add two matrices
print("Addition of m1 and m2:")
print(m1 + m2)

# Multiply two matrices (component-by-component)
print("Component-by-component multiplication of m1 and m2:")
print(m1 * m2)

# Matrix multiplication
print("Matrix multiplication of m1 and m2:")
print(m1 @ m2)
