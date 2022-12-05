#! /home/jscott/.pyenv/shims/python

from sys import argv
from typing import List
from pprint import pp


# a little ick
def parse_crates(input_lines: List[str]) -> List[List[str]]:
    crates = []

    previous_line = ""
    for line in input_lines:
        if line == "":
            break
        previous_line = line

    stack_limit = int(list(filter(lambda x: x != "", list(previous_line)))[-1])

    for line in input_lines:
        if line == "":
            break
        line_chunks = list(line)

        stack = [""] * stack_limit
        j = 0
        for i in range(1, len(line_chunks), 4):
            stack[j] = line_chunks[i].strip()
            j += 1

        crates.append(stack)

    crates.pop()

    # take array of rows and make array of cols
    crate_cols = []
    for i in range(stack_limit):
        crate_cols.append([])

    crates.reverse()
    for i in range(len(crates)):
        for j in range(len(crates[i])):
            if crates[i][j] == "":
                continue
            crate_cols[j].append(crates[i][j])

    return crate_cols


def prompt_one(input_lines: List[str]):
    crate_stacks = parse_crates(input_lines)

    # only work on moves
    move_line = False
    for move in input_lines:
        if not move_line:
            if move == "":
                move_line = True
            continue

        (_, amount, _, from_column, _, to_column) = move.split(" ")

        stack = []
        for i in range(int(amount)):
            stack.append(crate_stacks[int(from_column) - 1].pop())
            crate_stacks[int(to_column) - 1].append(stack.pop())

    return "".join(list(map(lambda x: x.pop(), crate_stacks)))


def prompt_two(input_lines: List[str]):
    crate_stacks = parse_crates(input_lines)

    # only work on moves
    move_line = False
    for move in input_lines:
        if not move_line:
            if move == "":
                move_line = True
            continue

        (_, amount, _, from_column, _, to_column) = move.split(" ")

        stack = []
        for i in range(int(amount)):
            stack.append(crate_stacks[int(from_column) - 1].pop())
        for i in range(int(amount)):
            crate_stacks[int(to_column) - 1].append(stack.pop())

    return "".join(list(map(lambda x: x.pop(), crate_stacks)))


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
