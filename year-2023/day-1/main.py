#! /home/jscott/.pyenv/shims/python

from sys import argv
from typing import List, Dict


def find_digit(line: str) -> int:
    # find the first digit
    first_digit = ""

    for c in line:
        if c.isdigit():
            first_digit = c
            break

    # find the last digit
    last_digit = ""
    for c in line[::-1]:
        if c.isdigit():
            last_digit = c
            break

    return int(first_digit + last_digit)


def prompt_one(input_lines: List[str]):
    answer = 0

    for l in input_lines:
        answer += find_digit(l)

    return answer


def find_all_substrings(string: str, sub: str) -> List[int]:
    indexes = []
    sub_len = len(sub)
    i = 0

    while i < len(string):
        if string[i:i + sub_len] == sub:
            indexes.append(i)
            i += sub_len
            continue

        i += 1

    return indexes


def find_digit_two(line: str, digit_map: Dict[str, str]) -> int:
    # go over the line and index each "digit"
    digit_arr = []  # [index, digit]

    for i, c in enumerate(line):
        if c.isdigit():
            digit_arr.append([i, c])

    for k, v in digit_map.items():
        # get index of the key values
        all_substring_indexes = find_all_substrings(line, k)

        for sub_i in all_substring_indexes:
            digit_arr.append([sub_i, v])

    # figure out which one is first
    sorted_digits = sorted(digit_arr, key=lambda x: x[0])

    return int(sorted_digits[0][1] + sorted_digits[-1][1])


def prompt_two(input_lines: List[str]):
    digit_map = {}
    digit_map["one"] = "1"
    digit_map["two"] = "2"
    digit_map["three"] = "3"
    digit_map["four"] = "4"
    digit_map["five"] = "5"
    digit_map["six"] = "6"
    digit_map["seven"] = "7"
    digit_map["eight"] = "8"
    digit_map["nine"] = "9"

    answer = 0

    for l in input_lines:
        answer += find_digit_two(l, digit_map)

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

    with open(problem_input, 'r') as f:
        input_lines = [line.rstrip() for line in f]

    if problem == "1":
        print(prompt_one(input_lines))
    else:
        print(prompt_two(input_lines))
