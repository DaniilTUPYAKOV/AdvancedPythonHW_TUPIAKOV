import sys
from collections.abc import Iterable

def process_lines(start_index: int, source: Iterable[str]):
    """Processing lines in iterable line source

    Args:
        start_index (int): start of numeration
        source (Iterable[str]): iterable source of lines (str type)
    """
    index = start_index
    for line in source:
        formatted_print(index, line)
        index+=1

def formatted_print(number: int, text: str):
    """ Print given text with given number prefix in specified format

    Args:
        number (int): number to be printed as prefix for text
        text (str): text to be printed
    """
    space_for_digits_in_number = 6
    number_length = len(str(number))
    prefix = ""

    if number_length <= space_for_digits_in_number:
        prefix = "".join([" "]*(space_for_digits_in_number-number_length))

    print(f'{prefix}{number}  {text}', end="")

def simple_nl_in_python():
    """ Emulating `nl -b a` linux command
    """
    start_index = 1
    source = []
    if len(sys.argv) == 1:
        source = sys.stdin
    else:
        for filename in sys.argv[1:]:
            with open(filename, 'r',encoding="UTF-8") as file:
                source+=file.readlines()
                file.close()

    process_lines(start_index, source)

if __name__ == '__main__':
    simple_nl_in_python()
