#! /home/jscott/.pyenv/shims/python

from sys import argv
from typing import List, Tuple


def get_gamma_and_epsilon(bit_map: List[str]) -> Tuple[str]:
    gamma_string = "0b"
    epsilon_string = "0b"

    for bit in bit_map:
        if bit > 0:
            gamma_string += "1"
            epsilon_string += "0"
        else:
            gamma_string += "0"
            epsilon_string += "1"

    return (int(gamma_string, base=2), int(epsilon_string, base=2))


def prompt_one(input_lines: List[str]):
    # find the most common bit in each column
    length_of_row = len(input_lines[0])

    bit_map = [0] * length_of_row

    position = 0
    for line in input_lines:
        for bit in line:
            if bit == "1":
                bit_map[position] += 1
            else:
                bit_map[position] -= 1
            position += 1
        position = 0

    [gamma, epsilon] = get_gamma_and_epsilon(bit_map)

    return gamma * epsilon


def get_oxygen_rating(input_lines: List[str]) -> int:
    length_of_row = len(input_lines[0])
    common_tracker = 0
    tracking_numbers = input_lines

    for i in range(length_of_row):
        if len(tracking_numbers) == 1:
            break

        for line in tracking_numbers:
            if line[i] == "1":
                common_tracker += 1
            else:
                common_tracker -= 1

        common_bit = "1" if common_tracker >= 0 else "0"

        tracking_numbers = list(filter(
            lambda line: line[i] == common_bit, tracking_numbers))

        common_tracker = 0
    return int(f'0b{tracking_numbers[0]}', base=2)


def get_co2_rating(input_lines: List[str]) -> int:
    length_of_row = len(input_lines[0])
    common_tracker = 0
    tracking_numbers = input_lines

    for i in range(length_of_row):
        if len(tracking_numbers) == 1:
            break

        for line in tracking_numbers:
            if line[i] == "1":
                common_tracker += 1
            else:
                common_tracker -= 1

        common_bit = "1" if common_tracker >= 0 else "0"

        tracking_numbers = list(filter(
            lambda line: line[i] != common_bit, tracking_numbers))

        common_tracker = 0
    return int(f'0b{tracking_numbers[0]}', base=2)


def prompt_two(input_lines: List[str]):
    return get_oxygen_rating(input_lines) * get_co2_rating(input_lines)


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
