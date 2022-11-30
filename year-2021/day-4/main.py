#! /home/jscott/.pyenv/shims/python

from pprint import pp
from sys import argv
from typing import List, Tuple


def read_board(board_lines: List[str]) -> Tuple[List[str], List[str], List[str]]:
    rows = []
    cols = [[], [], [], [], []]
    all = []

    for line in board_lines:
        filtered_line = list(
            filter(lambda c: c != "" and c != " ", line.split(" ")))
        rows.append(filtered_line)
        i = 0
        for num in filtered_line:
            cols[i].append(num)
            all.append(num)
            i += 1

    return (rows, cols, all)


def find_solution_speed(board: Tuple[List[str], List[str], List[str]], draw: List[str]) -> int:
    solution_array = [i for i in draw[0:5]]
    solution_i = 5

    while solution_i < len(draw):
        for row in board[0]:
            solution_temp = list(
                filter(lambda num: num in solution_array, row))
            if len(solution_temp) == 5:
                return len(solution_array)

        for col in board[1]:
            solution_temp = list(
                filter(lambda num: num in solution_array, col))
            if len(solution_temp) == 5:
                return len(solution_array)

        solution_array.append(draw[solution_i])
        solution_i += 1
    return -1


def solution(board, last_number, lookup_sequence):
    return sum(list(map(lambda n: int(n, base=10), list(
        filter(lambda n: not n in lookup_sequence, board[2]))))) * int(last_number)


def prompt_one(input_lines: List[str]):
    draw_sequence = input_lines[0].split(",")

    start = 2
    boards = []
    while start < len(input_lines) - 1:
        boards.append(read_board(input_lines[start:start + 5]))
        start += 6

    fastest_board = None
    fastest_board_speed = 99999999999999999

    for board in boards:
        solution_speed = find_solution_speed(board, draw_sequence)
        if solution_speed < fastest_board_speed:
            fastest_board_speed = solution_speed
            fastest_board = board

    return solution(fastest_board, draw_sequence[fastest_board_speed - 1], {
        draw_sequence[i]: True for i in range(fastest_board_speed)
    })


def prompt_two(input_lines: List[str]):
    draw_sequence = input_lines[0].split(",")

    start = 2
    boards = []
    while start < len(input_lines) - 1:
        boards.append(read_board(input_lines[start:start + 5]))
        start += 6

    slowest_board = None
    slowest_board_speed = -2

    for board in boards:
        solution_speed = find_solution_speed(board, draw_sequence)
        if solution_speed > slowest_board_speed:
            slowest_board_speed = solution_speed
            slowest_board = board

    return solution(slowest_board, draw_sequence[slowest_board_speed - 1], {
        draw_sequence[i]: True for i in range(slowest_board_speed)
    })


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
