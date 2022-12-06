#! /home/jscott/.pyenv/shims/python

from sys import argv
from typing import List


def process_packet(packet: str, characters: int) -> int:
    answer = characters
    processed_characters = []
    current_window = dict()

    # preprocess
    for character in packet[:characters]:
        if not character in current_window:
            current_window[character] = 0

        current_window[character] += 1
        processed_characters.append(character)

    for character in packet[characters:]:
        if len(current_window.keys()) == characters:
            return answer

        # delete the character in that left the window
        out_of_window = processed_characters.pop(0)
        current_window[out_of_window] -= 1

        if current_window[out_of_window] == 0:
            del current_window[out_of_window]

        # add the current character to the window
        if not character in current_window:
            current_window[character] = 0

        current_window[character] += 1

        processed_characters.append(character)

        answer += 1

    return answer


def prompt_one(input_lines: List[str]):
    packet = list(input_lines[0])

    return process_packet(packet, 4)


def prompt_two(input_lines: List[str]):
    packet = list(input_lines[0])

    return process_packet(packet, 14)


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
