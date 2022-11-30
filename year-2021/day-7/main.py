#! /home/jscott/.pyenv/shims/python

from sys import argv, setrecursionlimit
from typing import List, Dict


def fill_in_fuel_map_one(fuel_map: List[int], position: int):
    for i in range(len(fuel_map)):
        fuel_map[i] += abs(position - i)


def prompt_one(input_lines: List[str]):
    positions = list(map(lambda x: int(x), input_lines[0].split(",")))
    max_position = max(positions)
    fuel_map = [0] * max_position

    for position in positions:
        fill_in_fuel_map_one(fuel_map, position)

    return min(fuel_map)


def crab_fuel_rec(n: int, cache: Dict[int, int]) -> int:
    if not n in cache:
        cache[n] = n + crab_fuel_rec(n - 1, cache)

    return cache[n]


def fill_in_fuel_map_two(fuel_map: List[int], position: int, cache: Dict[int, int]):
    for i in range(len(fuel_map)):
        fuel_map[i] += crab_fuel_rec(abs(position - i), cache)


def prompt_two(input_lines: List[str]):
    positions = list(map(lambda x: int(x), input_lines[0].split(",")))
    max_position = max(positions)
    fuel_map = [0] * max_position

    setrecursionlimit(2000) # needed because python is bad

    cache = {}
    cache[0] = 0
    cache[1] = 1

    for position in positions:
        fill_in_fuel_map_two(fuel_map, position, cache)

    return min(fuel_map)


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
