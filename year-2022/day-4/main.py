#! /home/jscott/.pyenv/shims/python

from sys import argv
from typing import List


def prompt_one(input_lines: List[str]):
    def clean(line):
        pairs = line.split(",")

        pairs = list(map(lambda x: x.split("-"), pairs))

        pairs[0] = list(map(lambda x: int(x, base=10), pairs[0]))
        pairs[1] = list(map(lambda x: int(x, base=10), pairs[1]))

        return pairs

    range_pairs = list(map(clean, input_lines))

    covered_pairs = 0

    for pair in range_pairs:
        (first_pair, second_pair) = pair

        # completely covered
        if first_pair[0] >= second_pair[0] and first_pair[1] <= second_pair[1]:
            covered_pairs += 1
            continue
        if first_pair[0] <= second_pair[0] and first_pair[1] >= second_pair[1]:
            covered_pairs += 1
            continue

    return covered_pairs


def prompt_two(input_lines: List[str]):
    def clean(line):
        pairs = line.split(",")

        pairs = list(map(lambda x: x.split("-"), pairs))

        pairs[0] = list(map(lambda x: int(x, base=10), pairs[0]))
        pairs[1] = list(map(lambda x: int(x, base=10), pairs[1]))

        return pairs

    range_pairs = list(map(clean, input_lines))

    covered_pairs = 0

    for pair in range_pairs:
        (first_pair, second_pair) = pair

        # completely covered
        if first_pair[0] >= second_pair[0] and first_pair[1] <= second_pair[1]:
            covered_pairs += 1
            continue
        if first_pair[0] <= second_pair[0] and first_pair[1] >= second_pair[1]:
            covered_pairs += 1
            continue
        # starting point is inside
        if first_pair[0] >= second_pair[0] and first_pair[0] <= second_pair[1]:
            covered_pairs += 1
            continue
        if second_pair[0] >= first_pair[0] and second_pair[0] <= first_pair[1]:
            covered_pairs += 1
            continue
        # ending point is inside
        if first_pair[1] >= second_pair[0] and first_pair[1] <= second_pair[1]:
            covered_pairs += 1
            continue
        if second_pair[1] >= first_pair[0] and second_pair[1] <= first_pair[1]:
            covered_pairs += 1
            continue

    return covered_pairs


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
