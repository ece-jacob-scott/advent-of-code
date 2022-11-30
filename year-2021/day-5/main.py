#! /home/jscott/.pyenv/shims/python

from sys import argv
from typing import List, Dict, Tuple
from math import dist
from pprint import pp
from functools import reduce


def add_points_to_map(points_map: Dict[str, int], points: Tuple[Tuple[int, int], Tuple[int, int]]) -> None:
    # create all the points to be added as array
    [x1, y1] = points[0]
    [x2, y2] = points[1]

    points_to_add = [i for i in points]

    x_diff = abs(x2 - x1)
    y_diff = abs(y2 - y1)

    # for now only consider rows and cols
    if x_diff != 0 and y_diff != 0:
        return

    x_start = x1 if x1 < x2 else x2
    y_start = y1 if y1 < y2 else y2

    for i in range(1, x_diff):
        points_to_add.append((x_start + i, y1))  # y1 = y2
    for i in range(1, y_diff):
        points_to_add.append((x1, y_start + i))  # x1 = x2

    # add all the points to the map
    for point in points_to_add:
        key = ",".join(map(lambda x: str(x), point))
        if not key in points_map:
            points_map[key] = 0
        points_map[key] += 1


def line_to_points(line: str) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    points_as_strings = line.split(" -> ")

    def turn_into_tuples(point: str):
        return tuple(map(lambda p: int(p, base=10), point.split(",")))

    return tuple(map(turn_into_tuples, points_as_strings))


def calculate_answer(points_map: Dict[str, int]) -> int:
    return reduce(
        lambda prev, curr: prev + 1 if curr > 1 else prev,
        points_map.values(),
        0)


def prompt_one(input_lines: List[str]) -> int:
    points_map = {}
    points = list(map(line_to_points, input_lines))

    for point in points:
        add_points_to_map(points_map, point)

    return calculate_answer(points_map)


def add_points_to_map_two(points_map: Dict[str, int], points: Tuple[Tuple[int, int], Tuple[int, int]]) -> None:
    # create all the points to be added as array
    [x1, y1] = points[0]
    [x2, y2] = points[1]

    points_to_add = [i for i in points]

    x_diff = abs(x2 - x1)
    y_diff = abs(y2 - y1)

    if x_diff == y_diff:
        leftmost_point = points[0] if points[0][0] < points[1][0] else points[1]
        rightmost_point = points[1] if points[0][0] < points[1][0] else points[0]

        # build the points between the lines now
        # find the leftmost point
        above = leftmost_point[1] < rightmost_point[1]
        diff = x_diff  # x_diff == y_diff

        for i in range(1, diff):
            if above:
                points_to_add.append(
                    (leftmost_point[0] + i, leftmost_point[1] + i))
            else:
                points_to_add.append(
                    (leftmost_point[0] + i, leftmost_point[1] - i))
    else:
        x_start = x1 if x1 < x2 else x2
        y_start = y1 if y1 < y2 else y2

        for i in range(1, x_diff):
            points_to_add.append((x_start + i, y1))  # y1 = y2
        for i in range(1, y_diff):
            points_to_add.append((x1, y_start + i))  # x1 = x2

    # add all the points to the map
    for point in points_to_add:
        key = ",".join(map(lambda x: str(x), point))
        if not key in points_map:
            points_map[key] = 0
        points_map[key] += 1


def prompt_two(input_lines: List[str]):
    points_map = {}
    points = list(map(line_to_points, input_lines))

    for point in points:
        add_points_to_map_two(points_map, point)

    return calculate_answer(points_map)


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
