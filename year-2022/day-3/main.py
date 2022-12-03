#! /home/jscott/.pyenv/shims/python

from sys import argv
from typing import List
from functools import reduce
from pprint import pp


def score(item: str) -> int:
    if item.capitalize() == item:
        return ord(item) - 64 + 26
    else:
        return ord(item) - 96


# use a set to get O(1) lookup time and loop through half the rucksack to
# populate the set and then loop through the other half to find the matching
# item
def prompt_one(input_lines: List[str]):
    rucksacks = list(map(lambda x: list(x), input_lines))

    wrong_items = []

    for rucksack in rucksacks:
        item_set = set()
        half = round(len(rucksack) / 2)

        for i in range(half):
            item_set.add(rucksack[i])

        for i in range(half):
            if rucksack[i + half] in item_set:
                wrong_items.append(rucksack[i + half])
                break

    return sum(map(lambda x: score(x), wrong_items))


# use 2 sets to get O(1) lookup time and populate both set's with the contents
# of the first 2 groups in their corresponding sets and then with the last group
# find out if any item is in both sets, that item is the badge
def prompt_two(input_lines: List[str]):
    rucksacks = list(map(lambda x: list(x), input_lines))

    badges = []

    for i in range(0, len(rucksacks), 3):
        group = rucksacks[i:i+3]
        group_sets = [set(), set()]

        for i in range(2):
            for item in group[i]:
                group_sets[i].add(item)

        for item in group[2]:
            if item in group_sets[0] and item in group_sets[1]:
                badges.append(item)
                break

    return sum(map(lambda x: score(x), badges))


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
