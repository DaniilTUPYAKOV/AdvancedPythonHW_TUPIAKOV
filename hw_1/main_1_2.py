import sys
from collections.abc import Iterable

def process_lines(source: Iterable[str]):
    """Processing lines in iterable line source

    Args:
        source (Iterable[str]): iterable source of lines (str type)
    """
    for line in source:
        print(line, end="")

def print_filename(filename: str):
    """ Print given filename in specified format

    Args:
        filename (str): filename
    """

    print(f'==> {filename} <==')

def simple_tail_in_python():
    """ Emulating `tail` linux command
    """

    if len(sys.argv) == 1:
        process_lines(sys.stdin.readlines()[-17:])
    else:
        print_name = False
        if len(sys.argv[1:]) > 1:
            print_name = True
        for filename in sys.argv[1:]:

            with open(filename, 'r', encoding="UTF-8") as file:
                if print_name:
                    print_filename(filename)

                source = file.readlines()
                file.close()
                process_lines(source[-10:])


if __name__ == '__main__':
    simple_tail_in_python()
