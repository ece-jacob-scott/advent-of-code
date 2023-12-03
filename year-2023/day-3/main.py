#! /home/jscott/.pyenv/shims/python

from sys import argv
from typing import List, Dict, Set, Tuple
from pprint import pprint
from operator import mul
from functools import reduce


def check_for_symbol(symbol_coordinates: Set[Tuple[int, int]],
                     y: int,
                     x: int):
    check = False

    check = check or (y - 1, x) in symbol_coordinates
    check = check or (y + 1, x) in symbol_coordinates
    check = check or (y - 1, x - 1) in symbol_coordinates
    check = check or (y, x - 1) in symbol_coordinates
    check = check or (y + 1, x - 1) in symbol_coordinates
    check = check or (y - 1, x + 1) in symbol_coordinates
    check = check or (y, x + 1) in symbol_coordinates
    check = check or (y + 1, x + 1) in symbol_coordinates

    return check


def walk_line(lines: List[List[str]],
              symbol_coordinates: Set[Tuple[int, int]],
              y: int) -> List[int]:
    part_numbers = []

    number_str = ""
    add_part = False

    for x, c in enumerate(lines[y]):
        if c.isdigit():
            number_str += c

            add_part = add_part or check_for_symbol(symbol_coordinates, y, x)

            continue

        if len(number_str) > 0:
            if add_part:
                part_numbers.append(int(number_str))

            number_str = ""
            add_part = False

    if len(number_str) > 0 and add_part:
        part_numbers.append(int(number_str))

    return part_numbers


def symbol_coordinates(lines: List[List[str]]) -> Set[Tuple[int, int]]:
    symbol_coords = set()

    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c.isdigit() or c == ".":
                continue
            symbol_coords.add((y, x))

    return symbol_coords


def prompt_one(input_lines: List[str]):
    part_numbers = []

    i = 0
    while i < len(input_lines):
        input_lines[i] = [*input_lines[i]]
        i += 1

    symbol_coords = symbol_coordinates(input_lines)

    for y, line in enumerate(input_lines):
        part_numbers.extend(walk_line(input_lines, symbol_coords, y))

    return sum(part_numbers)


def number_coordinates(input_lines: List[str]) -> Dict[Tuple[int, int], int]:
    parts = {}
    parsing = False
    right_edge = -1

    for y, line in enumerate(input_lines):
        line += "."  # makes my life easier
        for x, c in enumerate(line):
            if not parsing and c.isdigit():
                right_edge = x
                parsing = True

            if parsing and (not c.isdigit()):
                for i in range(right_edge, x):
                    parts[(y, i)] = int(line[right_edge:x])
                parsing = False

    # if parsing:
    #     for i in range(right_edge, len(input_lines[0])):
    #         parts[(y, i)] = int(line[right_edge:x])

    return parts


def prompt_two(input_lines: List[str]):
    answer = 0

    number_map = number_coordinates(input_lines)

    for y, line in enumerate(input_lines):
        for x, c in enumerate(line):
            if c != "*":
                continue
            gears = set()

            for diff_y in range(-1, 2):
                for diff_x in range(-1, 2):
                    check = (y + diff_y, x + diff_x)

                    if check in number_map:
                        gears.add(number_map[check])

            if len(gears) == 2:
                answer += reduce(mul, gears, 1)

    return answer


if __name__ == "__main__":
    if len(argv) != 3:
        print("use like './main.py {problem number} {environment}'")
        exit(1)

    [program_name, problem, environment] = argv

    if problem not in ["1", "2"]:
        print("problem must be in [1, 2]")
        exit(1)

    if environment not in ["test", "answer"]:
        print("environment must be in [test, answer]")
        exit(1)

    problem_input = f'{"test" if environment == "test" else "input"}-{problem}.txt'

    input_lines = []

    with open(problem_input, 'r') as f:
        input_lines = [line.rstrip() for line in f]

    if problem == "1":
        print(prompt_one(input_lines))
    else:
        print(prompt_two(input_lines))
