#! /home/jscott/.pyenv/shims/python

from sys import argv
from typing import List
from pprint import pp
from functools import cmp_to_key
from copy import deepcopy


def parse_line(line):
    curr_array = None
    arrays = {}
    array_counter = 0
    char_str = ""

    for i in range(len(line)):
        char = line[i]

        if char == ",":
            if char_str == "":
                continue
            curr_array.append(int(char_str))
            char_str = ""
            continue

        if char == "[":
            # need an array
            curr_array = []
            arrays[array_counter] = curr_array
            array_counter += 1
            continue

        if char == "]":
            if char_str != "":
                curr_array.append(int(char_str))
                char_str = ""
            array_counter -= 1
            if array_counter == 0:
                # end of the line
                return curr_array
            arrays[array_counter - 1].append(curr_array)
            curr_array = arrays[array_counter - 1]
            continue
        char_str += char


def compare(pair, is_rec):
    (left, right) = pair

    while len(left) > 0 and len(right) > 0:
        # pop to get the values to be compared
        left_val = left.pop(0)
        right_val = right.pop(0)

        # if both values are ints then compare
        if isinstance(left_val, int) and isinstance(right_val, int):
            if left_val == right_val:

                continue
            return left_val < right_val

        # if isinstance(left_val, list) and isinstance(right_val, list):
        if isinstance(left_val, list) and isinstance(right_val, list):
            compare_result = compare([left_val, right_val], True)
            if compare_result == None:
                continue
            return compare_result

        # if one is not a list then make it a list and compare
        if isinstance(left_val, list):
            compare_result = compare([left_val, [right_val]], True)
            if compare_result == None:
                continue
            return compare_result

        if isinstance(right_val, list):
            compare_result = compare([[left_val], right_val], True)
            if compare_result == None:
                continue
            return compare_result

    if (len(left) == len(right)) and is_rec:
        return None
    return len(left) < len(right)


def prompt_one(input_lines: List[str]):
    pair = []
    pair_index = 1
    correct_order_pairs = []
    input_lines.append("")

    for line in input_lines:
        if line == "":
            # compare here
            if compare(pair, False):
                correct_order_pairs.append(pair_index)
            pair_index += 1
            pair = []
            continue
        parsed_line = parse_line(line)
        pair.append(parsed_line)

    return sum(correct_order_pairs)


def compare_sorted(left, right):
    left_deep_copy = deepcopy(left)
    right_deep_copy = deepcopy(right)
    return -1 if compare([left_deep_copy, right_deep_copy], False) else 1


def prompt_two(input_lines: List[str]):
    input_lines.append("[[2]]")
    input_lines.append("[[6]]")

    parsed_lines = []
    for line in input_lines:
        if line == "":
            continue
        parsed_lines.append(parse_line(line))

    sorted_list = sorted(parsed_lines, key=cmp_to_key(compare_sorted))

    start_index = 0

    for i in range(len(sorted_list)):
        array = sorted_list[i]
        if array == [[2]]:
            start_index = i + 1
        if array == [[6]]:
            return (i + 1) * start_index


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
