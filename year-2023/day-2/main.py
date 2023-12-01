#! /home/jscott/.pyenv/shims/python

from sys import argv
from typing import List, Dict

block_limit_one = {
    "red": 12,
    "green": 13,
    "blue": 14
}


# returns a list of the numbers [red, green, blue]
def get_max_pulled_one(game: str) -> Dict[str, int]:
    color_maxes = {
        "red": 0,
        "green": 0,
        "blue": 0
    }

    # parse game into sets
    sets = map(lambda x: x.strip(), game.split(":")[1].strip().split(";"))

    for s in sets:
        # split to get numbers
        colors_w_numbers = map(lambda x: x.strip(), s.split(","))

        for c in colors_w_numbers:
            num = int(c.split(" ")[0])
            color = c.split(" ")[1]

            if color_maxes[color] < num:
                color_maxes[color] = num

    return color_maxes


def prompt_one(input_lines: List[str]):
    answer = 0

    for line in input_lines:
        colors = get_max_pulled_one(line)

        red_ok = colors["red"] <= block_limit_one["red"]
        green_ok = colors["green"] <= block_limit_one["green"]
        blue_ok = colors["blue"] <= block_limit_one["blue"]

        if red_ok and green_ok and blue_ok:
            answer += int(line.split(":")[0].split(" ")[1])

    return answer


def prompt_two(input_lines: List[str]):
    answer = 0

    for line in input_lines:
        colors = get_max_pulled_one(line)
        answer += (colors["red"] * colors["green"] * colors["blue"])

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

    with open(problem_input, 'r') as f:
        input_lines = [line.rstrip() for line in f]

    if problem == "1":
        print(prompt_one(input_lines))
    else:
        print(prompt_two(input_lines))
