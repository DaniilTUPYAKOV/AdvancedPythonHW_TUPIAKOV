""" Creation of LaTeX code for table """

from functools import wraps

def add_latex_document_structure(func):
    """ Decorator for adding simple necessary LaTeX project structure
    """
    @wraps(func)
    def inner(*args, **kwargs):
        start_code = "\\documentclass{article}\n\\usepackage{graphicx}\n\\begin{document}\n"
        end_code = "\n\\end{document}"
        return start_code + func(*args, **kwargs) + end_code
    return inner

@add_latex_document_structure
def generate_latex_table(input_data: list[list]) -> str:
    """ Generate LaTeX code for table with given data

    Args:
        input_data (list[list]): List of lists with table data

    Returns:
        str: LaTeX code for table with given data
    """

    table_start = "\\begin{tabular}{|" + "c|" * \
        len(input_data[0]) + "}\n\\hline\n"
    table_end = "\\end{tabular}"

    def add_row(row_data: list) -> str:
        return " & ".join(map(str, row_data)) + " \\\\\n\\hline\n"

    result_line = (
        table_start
        + "".join(list(map(add_row, input_data)))
        + table_end
    )

    return result_line
