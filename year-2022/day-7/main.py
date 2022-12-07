#! /home/jscott/.pyenv/shims/python

from sys import argv
from typing import List
from pprint import pp


def parse_line(line):
    parts = line.split(" ")

    if parts[0] == "$":
        if parts[1] == "ls":
            return (parts[1], None)
        return (parts[1], parts[2])

    return (parts[0], parts[1])


def create_node(name: str, parent):
    return {
        "name": name,
        "children": [],
        "parent": parent,
        "size": 0
    }


def __calculate_directory_sizes(node):
    if not node:
        return 0

    size = 0

    for child in node["children"]:
        if isinstance(child, int):
            size += child
            continue

        n = __calculate_directory_sizes(child)

        child["size"] += n
        size += n

    return size


def calculate_directory_sizes(file_system):
    __calculate_directory_sizes(file_system)

    for child in file_system["children"]:
        if isinstance(child, int):
            size = child
        else:
            size = child["size"]

        file_system["size"] += size


def __calculate_answer_rec(node, sizes):
    if not node:
        return

    for child in node["children"]:
        if isinstance(child, int):
            continue

        if child["size"] <= 100_000:
            sizes.append(child["size"])

        __calculate_answer_rec(child, sizes)


def calculate_answer(file_system):
    sizes = []

    __calculate_answer_rec(file_system, sizes)

    return sum(sizes)


def build_file_system(input_lines: List[str]):
    file_system = create_node("/", None)
    current_node = file_system

    for line in input_lines:
        (part_one, part_two) = parse_line(line)

        if part_one == "cd":
            if part_two == "/":
                current_node = file_system
            elif part_two == "..":
                current_node = current_node["parent"]
            else:
                new_node = None

                for child in current_node["children"]:
                    if isinstance(child, int):
                        continue
                    if child["name"] == part_two:
                        new_node = child
                        break

                if not new_node:
                    new_node = create_node(part_two, current_node)
                    current_node["children"].append(new_node)
                current_node = new_node
        elif part_one == "ls":
            continue
        else:
            if part_one[0] == "d":
                continue
            current_node["children"].append(int(part_one, base=10))

    return file_system


def prompt_one(input_lines: List[str]):
    file_system = build_file_system(input_lines)

    calculate_directory_sizes(file_system)

    return calculate_answer(file_system)


def __calculate_answer_two_rec(node, size_limit, sizes):
    if not node:
        return

    for child in node["children"]:
        if isinstance(child, int):
            continue

        if child["size"] >= size_limit:
            sizes.append(child["size"])

        __calculate_answer_two_rec(child, size_limit, sizes)


def calculate_answer_two(file_system):
    sizes = []

    __calculate_answer_two_rec(
        file_system, 30_000_000 - (70_000_000 - file_system["size"]), sizes)

    return min(sizes)


def prompt_two(input_lines: List[str]):
    file_system = build_file_system(input_lines)

    calculate_directory_sizes(file_system)

    return calculate_answer_two(file_system)


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
