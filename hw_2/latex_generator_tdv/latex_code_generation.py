""" Creation of LaTeX code for table """

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

def generate_latex_image(image_path: str, caption: str, label: str):
    """ Generates LaTeX code to include an image from the given path

    Args:
        image_path (str): The path to the image file

    Returns:
        str: A LaTeX code to include the image
    """

    result_line = ("\\begin{figure}[h!]\n"
                   + "\\centering\n"
                   + f"\\includegraphics{{{image_path}}}"
                   + f"\n\\caption{{{caption}}}\n"
                   + f"\\label{{{label}}}\n"
                   + "\\end{figure}")
    return result_line
