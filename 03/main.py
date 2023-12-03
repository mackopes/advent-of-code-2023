import numbers
from typing import Callable, Dict, Generator, List, Tuple


def is_symbol(char: str) -> bool:
    return char not in "0123456789."


def is_gear(char: str) -> bool:
    return char == "*"


Row = int
Column = int


def parse_parts(input_lines: List[str], is_part_func: Callable[[str], bool]) -> List[Tuple[Row, Column]]:
    parts: List[Tuple[Row, Column]] = []
    for row, line in enumerate(input_lines):
        for column, char in enumerate(line):
            if is_part_func(char):
                parts.append((row, column))

    return parts


def iter_numbers(input_line: str) -> Generator[Tuple[int, int, int], None, None]:
    number = ""
    start_col = -1
    for col, char in enumerate(input_line):
        if char.isdigit():
            if not number:
                start_col = col
            number += char
        elif number:
            yield (start_col, col-1, int(number))
            number = ""
            start_col = -1
    if number:
        yield (start_col, len(input_line)-1, int(number))


def part_is_close(row: Row, start_col: Column, end_col: Column, part: Tuple[Row, Column]) -> bool:
    part_row, part_col = part

    return row - 1 <= part_row <= row + 1 and start_col - 1 <= part_col <= end_col + 1

def is_part_number(row: Row, start_col: Column, end_col: Column, parts: List[Tuple[Row, Column]]) -> bool:
    return any(part_is_close(row, start_col, end_col, part) for part in parts)

def get_all_part_numbers(input_lines: List[str]) -> List[Tuple[Row, Column, Column, int]]:
    numbers: List[Tuple[Row, Column, Column, int]] = []

    for row, input_line in enumerate(input_lines):
        for start_col, end_col, number in iter_numbers(input_line):
            numbers.append((row, start_col, end_col, number))

    return numbers


def get_part_numbers(input_lines: List[str], parts: List[Tuple[Row, Column]]) -> List[int]:
    numbers = get_all_part_numbers(input_lines)
    numbers = [number[3] for number in numbers if is_part_number(*(number[:-1]), parts)]
    return numbers


def main():
    with open("input.txt") as f:
        input_lines = f.readlines()
        input_lines = [line.strip() for line in input_lines]

    parts = parse_parts(input_lines, is_symbol)
    numbers = get_part_numbers(input_lines, parts)

    print(sum(numbers))


def gear_ratio(gear: Tuple[Row, Column], numbers: List[Tuple[Row, Column, Column, int]]) -> int:
    # find adjacent numbers
    adjacent_numbers = []
    for number in numbers:
        if part_is_close(*number[:-1], gear):
            adjacent_numbers.append(number[3])

    # if there are exactly two, return the product
    if len(adjacent_numbers) == 2:
        return adjacent_numbers[0] * adjacent_numbers[1]
    else:
        return 0


def main_2():
    with open("input_small.txt") as f:
        input_lines = f.readlines()
        input_lines = [line.strip() for line in input_lines]

    gears = parse_parts(input_lines, is_gear)
    numbers = get_all_part_numbers(input_lines)

    ratios = [gear_ratio(gear, numbers) for gear in gears]
    print(sum(ratios))

if __name__ == "__main__":
    main_2()