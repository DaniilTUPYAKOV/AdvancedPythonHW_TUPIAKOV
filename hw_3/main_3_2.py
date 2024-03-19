import numpy as np


class GetterSetterMixin:

    def __getattr__(self, name):
        return self.__dict__.get(name, None)

    def __setattr__(self, name, value):
        self.__dict__[name] = value


class SaveToFileMixin:

    def save_to_file(self, file_name):
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(str(self))


class StrArrayLikeMixin:

    def __str__(self):
        result = []
        for _, value in self.__dict__.items():
            if isinstance(value, list):
                max_len = []
                for elem in zip(*value):
                    max_len.append(len(str(max(elem))))
                for elem in value:
                    temp_res = []
                    temp_res.append("[")
                    for i in range(len(elem)):
                        temp_res.append(
                            " " * (max_len[i] - len(str(elem[i]))) + str(elem[i])
                        )
                    temp_res.append("]")
                    result.append(" ".join(temp_res))
        return "[" + "\n ".join(result) + "]"


class Matrix(GetterSetterMixin, SaveToFileMixin, np.lib.mixins.NDArrayOperatorsMixin, StrArrayLikeMixin):

    def __init__(self, matrix):
        if isinstance(matrix, (list, tuple)):
            self.matrix = matrix
        else:
            raise ValueError("Init arguments should be an array-like structure")

    _HANDLED_TYPES = (list,)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs):
        out = kwargs.get("out", ())
        for x in inputs + out:
            if not isinstance(x, self._HANDLED_TYPES + (Matrix,)):
                return NotImplemented

        inputs = tuple(x.matrix if isinstance(x, Matrix) else x for x in inputs)
        if out:
            kwargs["out"] = tuple(x.matrix if isinstance(x, Matrix) else x for x in out)

        result = getattr(ufunc, method)(*inputs, **kwargs)

        if isinstance(result, tuple):
            return tuple(type(self)(x) for x in result)
        if method == "at":
            return None
        return type(self)(list(result))


np.random.seed(0)
matrix_a = Matrix(np.random.randint(0, 10, (10, 10)).tolist())
matrix_b = Matrix(np.random.randint(0, 10, (10, 10)).tolist())

(matrix_a + matrix_b).save_to_file("matrix+.txt")
(matrix_a * matrix_b).save_to_file("matrix_mult.txt")
(matrix_a @ matrix_b).save_to_file("matrix@.txt")
