#! /home/jscott/.pyenv/shims/python

from sys import argv
from typing import List, Tuple, Dict

key = {
    "A": "rock",
    "X": "rock",
    "Y": "paper",
    "B": "paper",
    "C": "scissors",
    "Z": "scissors"
}

# key beats value
results_map = {
    "paper": "rock",
    "rock": "scissors",
    "scissors": "paper"
}

# key loses to value
lose_map = {
    "rock": "paper",
    "scissors": "rock",
    "paper": "scissors"
}

throw_value = {
    "rock": 1,
    "paper": 2,
    "scissors": 3
}


def score(round: Tuple[str, str]) -> int:
    added_value = throw_value[round[1]]
    win = results_map[round[1]] == round[0]

    if win:
        return 6 + added_value
    elif round[0] == round[1]:
        return 3 + added_value
    else:
        return 0 + added_value


def prompt_one(input_lines: List[str]):
    rounds = list(map(
        lambda line:
        (key[line.split(" ")[0]], key[line.split(" ")[1]]), input_lines))

    return sum(map(lambda r: score(r), rounds))


def determine_throw(opponent_throw: str, outcome: str) -> str:
    if outcome == "Y":
        return opponent_throw
    if outcome == "X":
        return results_map[opponent_throw]
    if outcome == "Z":
        return lose_map[opponent_throw]


def prompt_two(input_lines: List[str]):
    rounds = list(map(
        lambda line:
        (key[line.split(" ")[0]], line.split(" ")[1]), input_lines))

    round_scores = []
    for round in rounds:
        r = (round[0], determine_throw(round[0], round[1]))
        round_scores.append(score(r))

    return sum(round_scores)


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
