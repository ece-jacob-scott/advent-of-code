#! /home/jscott/.pyenv/shims/python

from sys import argv
from typing import List, Tuple
from collections import namedtuple

Race = namedtuple("Race", ["time", "distance"])


def return_number_of_wins(race: Race) -> int:
    wins = 0

    speed = 0
    remaining_time = race.time
    distance = race.distance

    for _ in range(race.time):
        distance_traveled = speed * remaining_time

        if distance_traveled > distance:
            wins += 1

        speed += 1
        remaining_time -= 1

    return wins


def prompt_one(input_lines: List[str]):
    answer = 1
    races: List[Race] = []

    # parse time
    times = list(
        map(
            int,
            filter(lambda x: x != "", input_lines[0].split(":")[1].strip().split(" ")),
        )
    )
    # parse distance
    distances = list(
        map(
            int,
            filter(lambda x: x != "", input_lines[1].split(":")[1].strip().split(" ")),
        )
    )

    for i in range(len(times)):
        races.append(Race(times[i], distances[i]))

    for race in races:
        answer *= return_number_of_wins(race)

    return answer


def prompt_two(input_lines: List[str]):
    answer = 1
    races: List[Race] = []

    # parse time
    times = list(
        map(
            int,
            filter(lambda x: x != "", input_lines[0].split(":")[1].strip().split(" ")),
        )
    )
    # parse distance
    distances = list(
        map(
            int,
            filter(lambda x: x != "", input_lines[1].split(":")[1].strip().split(" ")),
        )
    )

    for i in range(len(times)):
        races.append(Race(times[i], distances[i]))

    for race in races:
        answer *= return_number_of_wins(race)

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

    with open(problem_input, "r") as f:
        input_lines = [line.rstrip() for line in f]

    if problem == "1":
        print(prompt_one(input_lines))
    else:
        print(prompt_two(input_lines))
