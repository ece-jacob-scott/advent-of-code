#! /home/jscott/.pyenv/shims/python

from sys import argv
from typing import List, Tuple
from pprint import pp
from math import floor


# return the new age of the fish and whether a new fish is created or not
def simulate_fish_one(fish: int) -> Tuple[int, bool]:
    if fish == 0:
        return (6, True)
    return (fish - 1, False)


def prompt_one(input_lines: List[str], days=80):
    lantern_fish = list(
        map(lambda lf: int(lf, base=10), input_lines[0].split(",")))

    for i in range(days):
        for j in range(len(lantern_fish)):
            fish = lantern_fish[j]

            (new_fish, create_new_fish) = simulate_fish_one(fish)

            lantern_fish[j] = new_fish

            if create_new_fish:
                lantern_fish.append(8)

    return len(lantern_fish)


def simulate_fish_two(groups: List[int]) -> None:
    new_fish = groups[0]

    for i in range(1, 9):
        groups[i - 1] = groups[i]

    groups[6] += new_fish
    groups[8] = new_fish


def prompt_two(input_lines: List[str]):
    lantern_fish = list(
        map(lambda lf: int(lf, base=10), input_lines[0].split(",")))

    groups = [0] * 9

    for fish in lantern_fish:
        groups[fish] += 1

    for i in range(256):
        simulate_fish_two(groups)

    return sum(groups)


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
