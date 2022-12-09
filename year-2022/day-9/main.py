#! /home/jscott/.pyenv/shims/python

from sys import argv
from typing import List, Dict, Set, Tuple
from pprint import pp


GRID_X = 80
GRID_Y = 50

START_X = round(GRID_X / 2)
START_Y = round(GRID_Y / 2)


def clear(area: List[List[str]]):
    for i in range(len(area)):
        for k in range(len(area[i])):
            area[i][k] = "-"


def tail_touching_head(
        positions: Dict[str, List[int]]) -> bool:
    head = positions["head"]
    tail = positions["tail"]
    # x and y can't be more than 1 from each other
    if abs(head[0] - tail[0]) <= 1 and abs(head[1] - tail[1]) <= 1:
        return True
    return False


def put_s(area: List[List[str]]):
    area[START_Y][START_X] = "s"


def move_tail(
        area: List[List[str]],
        positions: Dict[str, List[int]],
        step: Tuple[str, int],
        visited: Set[Tuple[int, int]]):
    if tail_touching_head(positions):
        return

    (direction, amount) = step

    # if the step is vertical then make sure it is aligned with the X axis
    if direction == "U" or direction == "D":
        positions["tail"][1] = positions["head"][1]

    # if the step is horizontal then make sure it is aligned with the Y axis
    if direction == "L" or direction == "R":
        positions["tail"][0] = positions["head"][0]

    for i in range(amount):
        if tail_touching_head(positions):
            return
        if direction == "U":
            positions["tail"][0] -= 1
        if direction == "D":
            positions["tail"][0] += 1
        if direction == "L":
            positions["tail"][1] -= 1
        if direction == "R":
            positions["tail"][1] += 1
        visited.add((positions["tail"][0], positions["tail"][1]))


def move_head(
        area: List[List[str]],
        positions: Dict[str, List[int]],
        step: Tuple[str, int]):
    (direction, amount) = step

    if direction == "U":
        positions["head"][0] -= amount
    elif direction == "D":
        positions["head"][0] += amount
    elif direction == "L":
        positions["head"][1] -= amount
    elif direction == "R":
        positions["head"][1] += amount


def put_x_and_y(area: List[List[str]], positions: Dict[str, List[int]]):
    head = positions["head"]
    tail = positions["tail"]
    area[tail[0]][tail[1]] = "T"
    area[head[0]][head[1]] = "H"


def prompt_one(input_lines: List[str]):
    steps = list(
        map(lambda x: (x[0], int(x[1])),
            map(lambda x: x.split(" "), input_lines)))
    visited = set()
    positions = {
        "head": [START_Y, START_X],
        "tail": [START_Y, START_X]
    }
    visited.add((positions["tail"][0], positions["tail"][1]))

    # just make a big grid to handle the motion
    area = [["-"] * GRID_X for i in range(GRID_Y)]

    # main loop
    s_test = steps
    for step in s_test:
        # apply the step to the head first
        move_head(area, positions, step)
        # apply successive steps and stop if tail is touching
        move_tail(area, positions, step, visited)

    return len(visited)


def add_positions_to_map(
        area: List[List[str]],
        positions: Dict[str, List[int]]):
    for (key, value) in positions.items():
        if key == "head":
            continue
        icon = key[-1]

        area[value[0]][value[1]] = icon
    area[positions["head"][0]][positions["head"][1]] = "H"


def print_grid(
        area: List[List[str]],
        positions: Dict[str, List[int]],
        visited: Set[Tuple[int, int]]):
    print("=" * 50)
    clear(area)

    for coor in visited:
        area[coor[0]][coor[1]] = "#"

    put_s(area)
    add_positions_to_map(area, positions)

    for row in area:
        for col in row:
            print(col, end="")
        print()


def move_tail_two(
        area: List[List[str]],
        positions: Dict[str, List[int]],
        step: Tuple[str, int],
        visited: Set[Tuple[int, int]]):
    if tail_touching_head(positions):
        return

    (_, amount) = step

    for i in range(amount):
        # determine how to move the tail
        (head_y, head_x) = positions["head"]
        (tail_y, tail_x) = positions["tail"]
        direction = ""
        if head_y < tail_y:
            # head is above tail
            direction += "U"
        elif head_y > tail_y:
            # head is below tail
            direction += "D"
        # else: head and tail same row

        if head_x < tail_x:
            # head is left of tail
            direction += "L"
        elif head_x > tail_x:
            # head is right of tail
            direction += "R"
        # else: head and tail same column

        if tail_touching_head(positions):
            return
        if "U" in direction:
            positions["tail"][0] -= 1
        if "D" in direction:
            positions["tail"][0] += 1
        if "L" in direction:
            positions["tail"][1] -= 1
        if "R" in direction:
            positions["tail"][1] += 1
        visited.add((positions["tail"][0], positions["tail"][1]))


def prompt_two(input_lines: List[str]):
    steps = list(
        map(lambda x: (x[0], int(x[1])),
            map(lambda x: x.split(" "), input_lines)))
    visited = set()
    positions = {
        "head": [START_Y, START_X],
        "tail_1": [START_Y, START_X],
        "tail_2": [START_Y, START_X],
        "tail_3": [START_Y, START_X],
        "tail_4": [START_Y, START_X],
        "tail_5": [START_Y, START_X],
        "tail_6": [START_Y, START_X],
        "tail_7": [START_Y, START_X],
        "tail_8": [START_Y, START_X],
        "tail_9": [START_Y, START_X],
    }
    visited.add((positions["tail_9"][0], positions["tail_9"][1]))
    area = [["-"] * GRID_X for i in range(GRID_Y)]

    step_test = steps
    for step in step_test:
        # move head
        move_head(area, positions, step)
        for i in range(step[1]):
            for i in range(9):
                head = f'tail_{i}'
                tail = f'tail_{i + 1}'
                if i == 0:
                    head = "head"
                move_tail_two(area,
                              {
                                  "head": positions[head],
                                  "tail": positions[tail]
                              },
                              (step[0], 1),
                              set() if not tail == "tail_9" else visited)
    return len(visited)


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
