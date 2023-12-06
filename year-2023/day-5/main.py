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

    # keep track of remaining source to test range against
    test_sources = [(source, source_range)]
    next_test_sources = []

    for line in almanac:
        destination_, source_, range_ = list(map(int, line.split(" ")))

        while len(test_sources) > 0:
            source, source_range = test_sources.pop(0)

            # figure out if source + source_range overlaps with source_ + range_
            high = min(source + source_range, source_ + range_)
            low = max(source, source_)

            # not in the overlapping range
            if high <= low:
                next_test_sources.append((source, source_range))
                continue

            # categorize overlap
            new_destination = -1
            new_range = -1

            # 1
            if high == (source + source_range) and low == source:
                new_destination = destination_ + (source - source_)
                new_range = source_range
                # no leftover
            # 2
            elif high == (source + source_range) and low == source_:
                new_destination = destination_
                new_range = (source + source_range) - source_
                # 1 leftover
                next_test_sources.append((source, source_ - source))
            # 3
            elif high == (source_ + range_) and low == source:
                new_destination = destination_ + (source - source_)
                new_range = (source_ + range_) - source
                # 1 leftover
                next_test_sources.append(
                    (source + new_range, (source + source_range) - (source_ + range_))
                )
            # 4
            elif high == (source_ + range_) and low == source_:
                new_destination = destination_
                new_range = range_
                # 2 leftover
                next_test_sources.append((source, source_ - source))
                next_test_sources.append(
                    (
                        source_ + new_range,
                        (source + source_range) - (source_ + new_range),
                    )
                )

            sources.append((new_destination, new_range))

        test_sources = next_test_sources
        next_test_sources = []

    if len(test_sources) > 0:
        sources.extend(test_sources)

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
            almanacs.append(almanac_input)
            almanac_input = []
            continue

        almanac_input.append(line)

    # - start with a single seed pair as the source
    # - run source_to_destination_two to get multiple more pairs
    # - run source_to_destination_two on those pairs to get more pairs
    # - repeat until there are no more almanacs
    # - the lowest number in the list of ranges should be the answer
    queue = seeds
    next_queue = []

    for almanac in almanacs:
        for seed_pair in queue:
            seed_source, seed_range = seed_pair
            new_source_ranges = source_to_destination_two(
                seed_source, seed_range, almanac[1:]
            )
            next_queue.extend(new_source_ranges)

        if len(next_queue) == 0:
            queue = queue
        else:
            queue = next_queue
            next_queue = []

    return min(queue, key=lambda x: x[0])[0]


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
