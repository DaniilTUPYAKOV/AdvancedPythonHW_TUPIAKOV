""" Main HW 2.1 module """

from latex_generator_tdv import generate_latex_table, generate_latex_image

if __name__ == "__main__":

    test_table = [
        ["Species / Year", "2021", "2022", "2023"],
        ["Cats", "171K", "201K", "257K"],
        ["Dogs", "158K", "196K", "216K"],
        ["Turtles", "15K", "19K", "21K"]
    ]

    START_CODE = "\\documentclass{article}\n\\usepackage{graphicx}\n\\begin{document}"
    END_CODE = "\\end{document}"

    with open("hw_2/artifacts/hw_2_2.tex", "w", encoding='utf-8') as file:
        file.write(
            START_CODE
            + "\n"
            + generate_latex_table(test_table)
            + "\n"
            + generate_latex_image(
                "test_image.jpg",
                "They're glad because IT WORKS!",
                "glad_cats"
            )
            + "\n"
            + END_CODE
        )
