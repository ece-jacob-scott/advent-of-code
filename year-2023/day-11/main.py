#! /home/jscott/.pyenv/shims/python

from pprint import pprint
from sys import argv
from typing import List, Set


def get_empty_rows(map: List[List[str]]) -> Set[int]:
    rows = set()
    for i, row in enumerate(map):
        empty_row = True
        for col in row:
            if col != ".":
                empty_row = False
                break

        if empty_row:
            rows.add(i)

        empty_row = True

    return rows


def get_empty_cols(map: List[List[str]]) -> Set[int]:
    cols = set()
    num_of_cols = len(map[0])
    i = 0
    while i < num_of_cols:
        empty_col = True
        row = 0
        while row < len(map):
            if map[row][i] != ".":
                empty_col = False
                break
            row += 1

        if empty_col:
            cols.add(i)
        empty_col = False
        i += 1

    return cols


def calculate_distance(point_one, point_two) -> int:
    return abs(point_two["y"] - point_one["y"]) + abs(point_two["x"] - point_one["x"])


def prompt_one(input_lines: List[str]):
    # 1. get map into something useful
    map = []
    for line in input_lines:
        map.append(list(line))
    # 2. figure out which rows and cols are expanded
    empty_rows = get_empty_rows(map)
    empty_cols = get_empty_cols(map)
    # 3. get all the galaxies x,y with expansion
    galaxies = {}
    galaxy_i = 1
    x_expanded = 0
    y_expanded = 0
    for y, row in enumerate(map):
        if y in empty_rows:  # this is an expanded row so it counts for 2
            y_expanded += 1

        for x, col in enumerate(row):
            if x in empty_cols:
                x_expanded += 1

            if col == ".":
                x_expanded += 1
                continue

            galaxies[galaxy_i] = {"x": x_expanded, "y": y_expanded}
            galaxy_i += 1

            x_expanded += 1

        x_expanded = 0
        y_expanded += 1

    # pprint(galaxies)

    # 4. calculate path lengths get the shortest
    distances = []
    pairs = set()
    for key, value in galaxies.items():
        for _key, _value in galaxies.items():
            if key == _key:
                continue
            if f"{_key}_{key}" in pairs:
                continue
            # pprint(
            #     f"galaxy {key}({value}) -> {_key}({_value}) = {calculate_distance(value, _value)}"
            # )
            pairs.add(f"{key}_{_key}")
            distances.append(calculate_distance(value, _value))

    return sum(distances)


def prompt_two(input_lines: List[str]):
    # 1. get map into something useful
    map = []
    for line in input_lines:
        map.append(list(line))
    # 2. figure out which rows and cols are expanded
    empty_rows = get_empty_rows(map)
    empty_cols = get_empty_cols(map)
    # 3. get all the galaxies x,y with expansion
    galaxies = {}
    galaxy_i = 1
    x_expanded = 0
    y_expanded = 0
    for y, row in enumerate(map):
        if y in empty_rows:  # this is an expanded row so it counts for 1_000_000
            y_expanded += 999_999

        for x, col in enumerate(row):
            if x in empty_cols:
                x_expanded += 999_999

            if col == ".":
                x_expanded += 1
                continue

            galaxies[galaxy_i] = {"x": x_expanded, "y": y_expanded}
            galaxy_i += 1

            x_expanded += 1

        x_expanded = 0
        y_expanded += 1

    # pprint(galaxies)

    # 4. calculate path lengths get the shortest
    distances = []
    pairs = set()
    for key, value in galaxies.items():
        for _key, _value in galaxies.items():
            if key == _key:
                continue
            if f"{_key}_{key}" in pairs:
                continue
            # pprint(
            #     f"galaxy {key}({value}) -> {_key}({_value}) = {calculate_distance(value, _value)}"
            # )
            pairs.add(f"{key}_{_key}")
            distances.append(calculate_distance(value, _value))

    return sum(distances)


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

    with open(problem_input, "r") as f:
        input_lines = [line.rstrip() for line in f]

    if problem == "1":
        print(prompt_one(input_lines))
    else:
        print(prompt_two(input_lines))
