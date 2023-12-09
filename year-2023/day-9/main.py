#! /home/jscott/.pyenv/shims/python

from sys import argv
from typing import List
from pprint import pprint


def every(lst: List[int], cmp: int) -> bool:
    for i in lst:
        if i != cmp:
            return False
    return True


def continue_sequence(sequence: List[int]) -> int:
    answer = -1
    history = [sequence]
    current = sequence

    while not every(current, 0):
        new = []

        i = 0
        while i < (len(current) - 1):
            new.append(current[i + 1] - current[i])
            i += 1

        current = new
        history.append(new)

    addition_value = 0
    i = len(history) - 1
    while i >= 0:
        new_value = history[i][-1] + addition_value
        history[i].append(new_value)
        addition_value = new_value
        i -= 1

    return history[0][-1]


def prompt_one(input_lines: List[str]):
    answer = []

    for line in input_lines:
        answer.append(continue_sequence(list(map(int, line.split(" ")))))

    return sum(answer)


def backwards_sequence(sequence: List[int]) -> int:
    answer = -1
    history = [sequence]
    current = sequence

    while not every(current, 0):
        new = []

        i = 0
        while i < (len(current) - 1):
            new.append(current[i + 1] - current[i])
            i += 1

        current = new
        history.append(new)

    addition_value = 0
    i = len(history) - 1
    while i >= 0:
        new_value = history[i][-1] + addition_value
        history[i].append(new_value)
        addition_value = new_value
        i -= 1

    return history[0][-1]


def prompt_two(input_lines: List[str]):
    answer = []

    for line in input_lines:
        answer.append(
            backwards_sequence(list(reversed(list(map(int, line.split(" "))))))
        )

    return sum(answer)


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
