#! /home/jscott/.pyenv/shims/python

from sys import argv
from typing import List
from pprint import pp


def parse_line(line):
    curr_array = None
    arrays = {}
    array_counter = 0

    for i in range(len(line)):
        char = line[i]

        if char == ",":
            continue

        if char == "[":
            # need an array
            curr_array = []
            arrays[array_counter] = curr_array
            array_counter += 1
            continue

        if char == "]":
            array_counter -= 1
            if array_counter == 0:
                # end of the line
                return curr_array
            arrays[array_counter - 1].append(curr_array)
            curr_array = arrays[array_counter - 1]
            continue

        curr_array.append(int(char))


def handle_ints(pair):
    (left, right) = pair
    if left == right:
        return None
    return left < right


def handle_arrays(pair):
    (left, right) = pair

    while len(left) > 0 and len(right) > 0:
        left_value = left.pop(0)
        right_value = right.pop(0)

        if isinstance(left_value, int) and isinstance(right_value, int):
            c = handle_ints([left_value, right_value])
            if not c == None:
                return c
            continue

        if isinstance(left_value, list) and isinstance(right_value, list):
            c = handle_arrays([left_value, right_value])
            if not c == None:
                return c
            continue

        if isinstance(left_value, list):
            c = handle_arrays([left_value, [right_value]])
        if isinstance(right_value, list):
            c = handle_arrays([[left_value], right_value])
        if not c == None:
            return c

    if len(left) == len(right):
        return None

    return len(left) < len(right)


def comparison(pair, is_rec):
    c = handle_arrays(pair)
    (left, right) = pair
    if c:
        return c
    return len(left) < len(right)


def prompt_one(input_lines: List[str]):
    pair = []
    pair_index = 1
    correct_order_pairs = []

    # input_lines = [input_lines[6], input_lines[7], ""]

    for line in input_lines:
        if line == "":
            # compare here
            if comparison(pair, False):
                correct_order_pairs.append(pair_index)
            pair_index += 1
            pair = []
            continue
        parsed_line = parse_line(line)
        pair.append(parsed_line)

    print(correct_order_pairs)

    return sum(correct_order_pairs)


def prompt_two(input_lines: List[str]):
    pass


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
