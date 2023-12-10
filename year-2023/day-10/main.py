#! /home/jscott/.pyenv/shims/python

from sys import argv
from typing import List, Tuple, Set
from pprint import pprint
from collections import defaultdict
from math import floor

VERTICAL = "|"
HORIZONTAL = "-"
BOT_LEFT = "L"
BOT_RIGHT = "J"
TOP_RIGHT = "7"
TOP_LEFT = "F"
GROUND = "."
START = "S"


valid_pipes = {
    "TOP": ["|", "7", "F", "S"],
    "BOTTOM": ["|", "J", "L", "S"],
    "LEFT": ["-", "L", "F", "S"],
    "RIGHT": ["-", "J", "7", "S"],
}

valid_moves = {
    "|": ["TOP", "BOTTOM"],
    "-": ["RIGHT", "LEFT"],
    "7": ["LEFT", "BOTTOM"],
    "L": ["TOP", "RIGHT"],
    "F": ["RIGHT", "BOTTOM"],
    "J": ["TOP", "LEFT"],
    "S": ["TOP", "BOTTOM", "LEFT", "RIGHT"],
}

cardinal_coors = {"TOP": (-1, 0), "BOTTOM": (1, 0), "LEFT": (0, -1), "RIGHT": (0, 1)}

oppisite_direction = {
    "LEFT": "RIGHT",
    "RIGHT": "LEFT",
    "TOP": "BOTTOM",
    "BOTTOM": "TOP",
}


def find_moves(
    pipes: List[List[str]], current: Tuple[int, int]
) -> List[Tuple[int, int, str]]:
    y, x = current
    current_pipe = pipes[y][x]
    moves = []

    candidate_moves = valid_moves[current_pipe]

    for direction in candidate_moves:
        coors = cardinal_coors[direction]

        if pipes[y + coors[0]][x + coors[1]] not in valid_pipes[direction]:
            continue

        moves.append((y + coors[0], x + coors[1], direction))

    return moves


def traverse_pipes(pipes) -> int:
    starting = ""

    i = 0
    while i < len(pipes):
        j = 0
        while j < len(pipes[0]):
            if pipes[i][j] == START:
                starting = (i, j)
                break
            j += 1
        if starting != "":
            break
        i += 1

    moves = find_moves(pipes, starting)
    moves = moves[:1]
    moves_num = 1

    while len(moves) != 0:
        move = moves.pop(0)
        y, x, direction = move

        if pipes[y][x] == START:
            break

        candidate_moves = find_moves(pipes, (y, x))

        for candidate in candidate_moves:
            if direction == oppisite_direction[candidate[2]]:
                continue
            moves.append(candidate)

        moves_num += 1

    return moves_num


def prompt_one(input_lines: List[str]):
    answer = 0
    pipes = []

    for line in input_lines:
        line = list(line)
        line = ["."] + line[:] + ["."]
        pipes.append(line)

    pipes = [(["."] * len(pipes[0]))] + pipes[:]
    pipes.append(["."] * len(pipes[0]))

    answer = traverse_pipes(pipes)

    return floor(answer / 2)


def traverse_pipes_two(pipes) -> Set[Tuple[int, int]]:
    starting = ""
    visited = set()

    i = 0
    while i < len(pipes):
        j = 0
        while j < len(pipes[0]):
            if pipes[i][j] == START:
                starting = (i, j)
                break
            j += 1
        if starting != "":
            break
        i += 1

    moves = find_moves(pipes, starting)
    moves = moves[:1]

    while len(moves) != 0:
        move = moves.pop(0)
        y, x, direction = move
        visited.add((y, x))

        if pipes[y][x] == START:
            break

        candidate_moves = find_moves(pipes, (y, x))

        for candidate in candidate_moves:
            if direction == oppisite_direction[candidate[2]]:
                continue
            moves.append(candidate)

    return visited


def calculate_enclosed_ground(
    pipes: List[List[str]], visited: Set[Tuple[int, int]]
) -> int:
    ground_captured = 0
    searching = False
    capture_pipe = set(["|", "F", "J", "L", "7", "S"])
    stop_pipe_map = {
        "|": ["|", "L", "F"],
        "L": ["J", "7"],
        "F": ["J", "7"],
        "S": ["J", "7"],
    }
    stop_pipe = []
    wall_stack = 0

    # for y, pipe_line in enumerate(pipes):
    #     for x, pipe in enumerate(pipe_line):
    #         if searching and pipe == GROUND:
    #             ground_captured += 1
    #             pipes[y][x] = "I"
    #             continue

    #         if pipe in capture_pipe and (y, x) in visited:
    #             # check if it should stop searching
    #             if searching and pipe in stop_pipe:
    #                 searching = False
    #                 stop_pipe = ""

    #                 if wall_stack > 0:
    #                     searching = True
    #                     stop_pipe = stop_pipe_map[VERTICAL]
    #                     wall_stack -= 1

    #                 continue

    #             # don't stop
    #             if searching:
    #                 continue

    #             # start searching
    #             if pipe == VERTICAL:
    #                 wall_stack += 1

    #             stop_pipe = stop_pipe_map[pipe]
    #             searching = True

    #     if searching:
    #         raise Exception("uh oh")

    return ground_captured


def prompt_two(input_lines: List[str]):
    answer = 0
    pipes = []

    for line in input_lines:
        line = list(line)
        line = ["."] + line[:] + ["."]
        pipes.append(line)

    pipes = [(["."] * len(pipes[0]))] + pipes[:]
    pipes.append(["."] * len(pipes[0]))

    visited = traverse_pipes_two(pipes)

    answer = calculate_enclosed_ground(pipes, visited)

    for line in pipes:
        print("".join(line))

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

    with open(problem_input, "r") as f:
        input_lines = [line.rstrip() for line in f]

    if problem == "1":
        print(prompt_one(input_lines))
    else:
        print(prompt_two(input_lines))
