import sys
import os
from collections.abc import Iterable

class StatisticUnit:
    """ Data class for statistic data
    """
    number_of_lines: int
    number_of_words: int
    size_in_bytes: int
    filename: str

    def __init__(self, number_of_lines: int, number_of_words: int,
                 size_in_bytes: int, filename: str) -> None:
        self. number_of_lines = number_of_lines
        self.number_of_words = number_of_words
        self.size_in_bytes = size_in_bytes
        self.filename = filename

def print_statistic(result: list[StatisticUnit]):
    """ Print statistic data in specified format

    Args:
        result (list[StatisticUnit]): list of Statistic data objects
    """

    if not result[0].filename:
        print_statistic_line(result[0].number_of_lines,
                             result[0].number_of_words,
                             result[0].size_in_bytes)
    else:
        maximum_number = 0
        total_lines = 0
        total_words = 0
        total_size = 0

        for unit in result:
            maximum_number = max(maximum_number, unit.number_of_lines,
                                 unit.number_of_words, unit.size_in_bytes)
            total_lines+=unit.number_of_lines
            total_words+=unit.number_of_words
            total_size+=unit.size_in_bytes

        space_for_number = len(str(maximum_number))
        for unit in result:
            print_statistic_line(unit.number_of_lines,
                                 unit.number_of_words,
                                 unit.size_in_bytes,
                                 space_for_number)
            print(f' {unit.filename}')

        if len(result) > 1:
            print_statistic_line(total_lines,
                                 total_words,
                                 total_size,
                                 space_for_number)
            print(" total")


def print_statistic_line(number_of_lines: int, number_of_words: int,
                         size_in_bytes: int, space_for_digits: int = 7):
    """ Prints satatistic line, puts numbers in space with defined length

    Args:
        number_of_lines (int): number of lines
        number_of_words (int): _number of words
        size_in_bytes (int): size in bytes
        space_for_digits (int, optional): length of space for nuimbers. Defaults to 7.
    """
    number_of_lines_length = len(str(number_of_lines))
    number_of_words_length = len(str(number_of_words))
    number_of_bytes_length = len(str(size_in_bytes))

    print(f'{" "*(space_for_digits-number_of_lines_length)}{number_of_lines} '
        + f'{" "*(space_for_digits-number_of_words_length)}{number_of_words} '
        + f'{" "*(space_for_digits-number_of_bytes_length)}{size_in_bytes}', end="")

def process_lines(source: Iterable[str], size: int = None) -> tuple:
    """Processing lines in iterable line source

    Args:
        source (Iterable[str]): iterable source of lines (str type)
        size (int): size of data in bytes, if None, than it should be
        calculated using source, default None
    """
    word_amount = 0
    for line in source:
        word_amount += len(line.split())

    if not size:
        size = len(("".join(source)).encode())

    return len(source), word_amount, size

def add_statistic_data(result: list[StatisticUnit], source: Iterable[str],
                       size: int = None, filename: str = None):
    """ Process data from source and add data to result list,
        if size is None calculate it from source data

    Args:
        result (list[StatisticUnit]): list of statistic data objects
        source (Iterable[str]): iterable source of str data
        size (int, optional): Size of sourse, calculates from source data if None. Defaults to None.
        filename (str, optional): name of file. Defaults to None.
    """
    lines, words, size = process_lines(source,  size)
    result.append(StatisticUnit(
        number_of_lines=lines,
        number_of_words=words,
        size_in_bytes=size,
        filename=filename
    ))

def simple_wc_in_python():
    """ Emulating `wc` linux command
    """
    result: Iterable[StatisticUnit] = []
    if len(sys.argv) == 1:
        add_statistic_data(result, sys.stdin.readlines())
    else:
        for filename in sys.argv[1:]:
            with open(filename, 'r', encoding="utf-8") as file:
                source = file.readlines()
                file.close()
                add_statistic_data(result, source, os.path.getsize(filename), filename)

    print_statistic(result)


if __name__ == '__main__':
    simple_wc_in_python()
