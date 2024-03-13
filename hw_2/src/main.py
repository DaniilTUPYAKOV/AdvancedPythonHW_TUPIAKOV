""" Main HW 2.1 module """

from tabel_creation import generate_latex_table

if __name__ == "__main__":

    test_table = [
        ["Species / Year", "2021", "2022", "2023"],
        ["Cats", "171K", "201K", "257K"],
        ["Dogs", "158K", "196K", "216K"],
        ["Turtles", "15K", "19K", "21K"]
    ]

    with open("hw_2/artifacts/hw_2_1_table.tex", "w", encoding='utf-8') as file:
        file.write(
            generate_latex_table(test_table)
        )
