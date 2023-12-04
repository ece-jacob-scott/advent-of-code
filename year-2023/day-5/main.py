#! /home/jscott/.pyenv/shims/python

from sys import argv
from typing import List, Dict, Tuple
from collections import defaultdict


# seeds: 79 14 55 13
def parse_seed_numbers(seed_line: str) -> List[int]:
    numbers = seed_line.split(":")[1].strip().split(" ")
    return list(map(int, numbers))


def source_to_destination(source: int, almanac: List[str]) -> int:
    for line in almanac:
        destination_, source_, range_ = list(map(int, line.split(" ")))

        if source >= source_ and source < (source_ + range_):
            return destination_ + (source - source_)

    return source


def prompt_one(input_lines: List[str]):
    answer = []
    seed_numbers = parse_seed_numbers(input_lines[0])

    input_lines.append("")  # makes parsing logic easier

    almanac_input = []
    almanacs = []
    for line in input_lines[2:]:
        if line == "":
            almanacs.append(almanac_input[1:])
            almanac_input = []
            continue

        almanac_input.append(line)

    for seed in seed_numbers:
        source = seed

        for almanac in almanacs:
            source = source_to_destination(source, almanac)

        answer.append(source)

    return min(answer)


def source_to_destination_two(
    source: int, source_range: int, almanac: List[str]
) -> List[Tuple[int, int]]:
    sources = []

    for line in almanac:
        destination_, source_, range_ = list(map(int, line.split(" ")))

        # figure out if source + source_range overlaps with source_ + range_
        # high = min(source + source_range, source_ + range_)
        # low = max(source, source_)

        # print(high, low)

        if high < low:
            continue

        sources.append((low, high - low))

    return sources


def parse_seed_numbers_two(seed_line: str) -> List[Tuple[int, int]]:
    numbers = list(map(int, seed_line.split(":")[1].strip().split(" ")))
    pairs = []

    for i in range(0, len(numbers), 2):
        pairs.append((numbers[i], numbers[i + 1]))

    return pairs


def prompt_two(input_lines: List[str]):
    answer = []
    seeds = parse_seed_numbers_two(input_lines[0])

    input_lines.append("")  # makes parsing logic easier

    almanac_input = []
    almanacs = []
    for line in input_lines[2:]:
        if line == "":
            almanacs.append(almanac_input[1:])
            almanac_input = []
            continue

        almanac_input.append(line)

    # - start with a single seed pair as the source
    # - run source_to_destination_two to get multiple more pairs
    # - run source_to_destination_two on those pairs to get more pairs
    # - repeat until there are no more almanacs
    # - the lowest number in the list of ranges should be the answer
    for seed_pair in seeds:
        queue = [seed_pair]
        next_queue = []

        for almanac in almanacs:
            for p in queue:
                new_sources = source_to_destination_two(p[0], p[1], almanac)
                next_queue.extend(new_sources)
            queue = next_queue
            next_queue = []

        print(queue)

    # return min(answer)


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

    with open(problem_input, "r") as f:
        input_lines = [line.rstrip() for line in f]

    if problem == "1":
        print(prompt_one(input_lines))
    else:
        print(prompt_two(input_lines))
