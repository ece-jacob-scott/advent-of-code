#! /home/jscott/.pyenv/shims/python

from sys import argv
from typing import List


def prompt_one(input_lines: List[str]):
    elf_calories = []

    elf_total = 0
    for line in input_lines:
        if line == "":
            elf_calories.append(elf_total)
            elf_total = 0
            continue
        elf_total += int(line, base=10)

    return max(elf_calories)


def prompt_two(input_lines: List[str]):
    elf_calories = []

    elf_total = 0
    for line in input_lines:
        if line == "":
            elf_calories.append(elf_total)
            elf_total = 0
            continue
        elf_total += int(line, base=10)

    return sum(sorted(elf_calories)[-3:])


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
