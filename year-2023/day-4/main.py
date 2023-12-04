#! /home/jscott/.pyenv/shims/python

from sys import argv
from typing import List
from collections import defaultdict


def process_card(line: str):
    card_value = 0
    winning_numbers = set(
        map(
            int,
            filter(
                lambda x: x != "",
                line.split(":")[1].split("|")[0].strip().split(" "),
            ),
        )
    )
    my_numbers = list(
        map(
            int,
            filter(
                lambda x: x != "",
                line.split(":")[1].split("|")[1].strip().split(" "),
            ),
        )
    )

    for n in my_numbers:
        if n in winning_numbers:
            if card_value == 0:
                card_value = 1
            else:
                card_value *= 2

    return card_value


def prompt_one(input_lines: List[str]):
    answer = 0

    for line in input_lines:
        answer += process_card(line)

    return answer


def process_card_two(line: str):
    card_value = 0
    winning_numbers = set(
        map(
            int,
            filter(
                lambda x: x != "",
                line.split(":")[1].split("|")[0].strip().split(" "),
            ),
        )
    )
    my_numbers = list(
        map(
            int,
            filter(
                lambda x: x != "",
                line.split(":")[1].split("|")[1].strip().split(" "),
            ),
        )
    )

    for n in my_numbers:
        if n in winning_numbers:
            card_value += 1

    return card_value


def prompt_two(input_lines: List[str]):
    answer = 0
    card_values = {}

    # pre fill in the card_values
    for line in input_lines:
        key = int(list(filter(lambda x: x != "", line.split(":")[0].split(" ")))[1])
        card_values[key] = process_card_two(line)

    copies = defaultdict(lambda: 1)

    for card in range(1, len(input_lines) + 1):
        value = card_values[card]

        for i in range(1, value + 1):
            copies[card + i] += copies[card]

        answer += copies[card]

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
