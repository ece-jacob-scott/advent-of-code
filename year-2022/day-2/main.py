#! /home/jscott/.pyenv/shims/python

from sys import argv
from typing import List, Tuple

key = {
    "A": "rock",
    "X": "rock",
    "Y": "paper",
    "B": "paper",
    "C": "scissors",
    "Z": "scissors"
}

win_map = {
    "rock": "paper",
    "paper": "scissors",
    "scissors": "rock"
}

lose_map = {
    "rock": "scissors",
    "paper": "rock",
    "scissors": "paper"
}

throw_value = {
    "rock": 1,
    "paper": 2,
    "scissors": 3
}


def score(round: Tuple[str, str]) -> int:
    if lose_map[round[1]] == round[0]:
        return 6 + throw_value[round[1]]
    elif round[0] == round[1]:
        return 3 + throw_value[round[1]]
    else:
        return 0 + throw_value[round[1]]


def prompt_one(input_lines: List[str]):
    rounds = list(map(
        lambda line:
        (key[line.split(" ")[0]], key[line.split(" ")[1]]), input_lines))

    return sum(map(lambda r: score(r), rounds))


def score_two(round: Tuple[str, str]) -> int:
    if round[1] == "Y":
        return 3 + throw_value[round[0]]
    elif round[1] == "X":
        return 0 + throw_value[lose_map[round[0]]]
    else:
        return 6 + throw_value[win_map[round[0]]]


def prompt_two(input_lines: List[str]):
    rounds = list(map(
        lambda line:
        (key[line.split(" ")[0]], line.split(" ")[1]), input_lines))

    return sum(map(lambda r: score_two(r), rounds))


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
