#! /home/jscott/.pyenv/shims/python

from sys import argv
from typing import List, Dict, Tuple
from math import lcm


def update_map(line: str, map_: Dict[str, Tuple[str, str]]):
    key = line.split(" = ")[0]
    pair = line.split(" = ")[1]

    # clean pair
    pair = pair.strip("(")
    pair = pair.strip(")")
    pair = pair.split(", ")

    map_[key] = (pair[0], pair[1])


def prompt_one(input_lines: List[str]):
    answer = 0
    steps = list(input_lines[0])
    map_ = {}

    # create map
    for line in input_lines[2:]:
        update_map(line, map_)

    current = "AAA"
    current_step = 0

    while current != "ZZZ":
        if steps[current_step] == "L":
            current = map_[current][0]
        else:
            current = map_[current][1]

        current_step += 1

        if current_step == len(steps):
            current_step = 0

        answer += 1

    return answer


def find_steady_state(
    start: str, steps: List[str], map_: Dict[str, Tuple[str, str]]
) -> int:
    answer = 0
    answers = []
    stop = 200
    current_step = 0
    current = start
    previous = 0

    while len(answers) != stop:
        if current[-1] == "Z":
            answers.append(answer - previous)
            previous = answer

        j = 0 if steps[current_step] == "L" else 1
        current = map_[current][j]

        current_step += 1

        if current_step == len(steps):
            current_step = 0

        answer += 1

    return answers[-1]


def prompt_two(input_lines: List[str]):
    answer = 0
    steps = list(input_lines[0])
    map_ = {}

    for line in input_lines[2:]:
        update_map(line, map_)

    current_step = 0
    starts = list(filter(lambda x: x[-1] == "A", map_.keys()))

    steady_states = []

    for start in starts:
        steady_states.append(find_steady_state(start, steps, map_))

    return lcm(*steady_states)


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
