#! /home/jscott/.pyenv/shims/python

from sys import argv
from typing import List
from math import floor


def prompt_one(input_lines: List[str]):
    instructions = input_lines
    clock = 1
    x_register = 1

    answer = 0
    next_checkpoint = 20
    answer = 0

    for instruction in instructions:
        cycles = 2 if instruction[:4] == "addx" else 1

        # start of the cycle so check for the answer
        for i in range(cycles):
            if clock == next_checkpoint:
                answer += clock * x_register
                next_checkpoint += 40

            clock += 1
            # after the clock cycle

        if instruction[:4] == "addx":
            x_register += int(instruction.split(" ")[1])

    return answer


def print_screen(screen):
    for i in range(0, 240, 40):
        print("".join(screen[i:i+40]))


def prompt_two(input_lines: List[str]):
    instructions = input_lines
    clock = 1
    x_register = 1
    screen = ["."] * 240

    answer = 0

    for instruction in instructions:
        cycles = 2 if instruction[:4] == "addx" else 1

        # start of the cycle so check for the answer
        for i in range(cycles):
            # draw a pixel
            sprite_bounds = [x_register - 1, x_register, x_register + 1]

            if (clock - 1) % 40 in sprite_bounds:
                screen[clock - 1] = "#"

            clock += 1
            # after the clock cycle

        if instruction[:4] == "addx":
            x_register += int(instruction.split(" ")[1])
    print_screen(screen)


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
