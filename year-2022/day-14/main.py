#! /home/jscott/.pyenv/shims/python

from sys import argv
from typing import List, Tuple
from pprint import pp


def get_dimensions(input_lines: List[str]) -> Tuple[int, int]:
    x_max = float("-inf")
    x_min = float("inf")
    y_max = float("-inf")
    y_min = float("inf")

    for line in input_lines:
        coors = tuple(map(
            lambda x: map(
                lambda k: int(k), x.split(",")), line.split(" -> ")))
        for coor in coors:
            (x, y) = coor
            if x < x_min:
                x_min = x
            if x > x_max:
                x_max = x
            if y < y_min:
                y_min = y
            if y > y_max:
                y_max = y

    # (x dimension, y dimension)
    return ((x_max, x_min), (y_max, y_min))


def print_board(board):
    i = 0
    for line in board:
        line_str = "".join(line)
        print(f'{i:03d} {line_str}')
        i += 1


def create_board(x_dim, y_dim):
    (x_max, x_min) = x_dim
    (y_max, y_min) = y_dim
    board = []

    # create board
    for i in range(y_max + 1):
        board.append(["." for k in range(x_max - x_min + 1)])

    # place start at 500, 0
    start_coor = (500 - x_min, 0)

    board[start_coor[1]][start_coor[0]] = "+"
    return (board, (start_coor[0], start_coor[1]))


def add_line_to_board(board, x_min, line, x_padding=0):
    # parse the line
    coors = tuple(map(
        lambda x: tuple(map(
            lambda k: int(k), x.split(","))), line.split(" -> ")))

    x_offset = x_min

    # (x, y)
    start_coor = coors[0]
    for coor in coors[1:]:
        (start_x, start_y) = start_coor
        (end_x, end_y) = coor

        # figure out if x or y line
        x_dist = end_x - start_x
        y_dist = end_y - start_y

        if x_dist == 0:
            up_or_down = -1 if y_dist < 0 else 1
            for i in range(abs(y_dist) + 1):
                board[start_y + (up_or_down * i)][(start_x -
                                                   x_offset) + x_padding] = "#"

        if y_dist == 0:
            left_or_right = -1 if x_dist > 0 else 1
            for i in range(abs(x_dist) + 1):
                board[start_y][((start_x - x_offset) +
                                x_padding) - (left_or_right * i)] = "#"

        start_coor = coor


def check_sand_space(board, sand_coor):
    (sand_x, sand_y) = sand_coor

    if board[sand_y + 1][sand_x] == ".":
        return "down"

    if board[sand_y + 1][sand_x - 1] == ".":
        return "left"

    if board[sand_y + 1][sand_x + 1] == ".":
        return "right"

    return None


def drop_sand(board, start_coor):
    # look down -> look left -> look right
    (sand_x, sand_y) = start_coor
    sand_y = sand_y + 1  # just under the starting position

    try:
        while direction := check_sand_space(board, (sand_x, sand_y)):
            if direction == "down":
                sand_y += 1
                continue

            if direction == "left":
                sand_y += 1
                sand_x -= 1
                continue

            if direction == "right":
                sand_y += 1
                sand_x += 1
                continue

        board[sand_y][sand_x] = "o"
    except IndexError:
        return "done"


def prompt_one(input_lines: List[str]):
    (x_dim, y_dim) = get_dimensions(input_lines)
    (x_max, x_min) = x_dim
    (y_max, y_min) = y_dim

    (board, start_coor) = create_board(x_dim, y_dim)

    for line in input_lines:
        add_line_to_board(board, x_min, line)

    sand = 0
    while drop_sand(board, start_coor) != "done":
        sand += 1

    return sand


def create_board_two(x_dim, y_dim, x_padding=20):
    (x_max, x_min) = x_dim
    (y_max, y_min) = y_dim
    board = []

    # create board
    for i in range(y_max + 1 + 1):
        board.append(["." for k in range(x_max - x_min + 1 + (2 * x_padding))])

    # place start at 500, 0
    start_coor = (500 - x_min + x_padding, 0)

    board[start_coor[1]][start_coor[0]] = "+"
    return (board, (start_coor[0], start_coor[1]))


def check_sand_space_two(board, sand_coor):
    (sand_x, sand_y) = sand_coor

    # stop at infinite wall
    if sand_y == (len(board) - 1):
        return None

    if board[sand_y + 1][sand_x] == ".":
        return "down"

    if board[sand_y + 1][sand_x - 1] == ".":
        return "left"

    if board[sand_y + 1][sand_x + 1] == ".":
        return "right"

    return None


def drop_sand_two(board, start_coor):
    # look down -> look left -> look right
    (sand_x, sand_y) = start_coor
    (end_x, end_y) = start_coor
    sand_y = sand_y

    while direction := check_sand_space_two(board, (sand_x, sand_y)):
        if direction == "down":
            sand_y += 1
            continue

        if direction == "left":
            sand_y += 1
            sand_x -= 1
            continue

        if direction == "right":
            sand_y += 1
            sand_x += 1
            continue

    board[sand_y][sand_x] = "o"

    # overall stop condition
    if sand_x == end_x and sand_y == end_y:
        return "done"


def prompt_two(input_lines: List[str]):
    (x_dim, y_dim) = get_dimensions(input_lines)
    (x_max, x_min) = x_dim
    (y_max, y_min) = y_dim

    padding = 10000

    (board, start_coor) = create_board_two(x_dim, y_dim, padding)

    for line in input_lines:
        add_line_to_board(board, x_min, line, padding)

    sand = 0
    while drop_sand_two(board, start_coor) != "done":
        sand += 1

    return sand + 1


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
