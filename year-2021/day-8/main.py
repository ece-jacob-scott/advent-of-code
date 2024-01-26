#! /home/jscott/.pyenv/shims/python

from sys import argv
from typing import List, Dict


def prompt_one(input_lines: List[str]):
    pass

# ; f = it's the only char that is in every line except one
# ; c = find 1 & 4 and c is the one they share that isn't f
# ; a = find 7 and a is whatever char remains besides c & f
# ; d = find 4 and all length 5 chars and the char they share is d
# ; b = find all length 5 and whatever char they don't have in common is b
# ; g = find all length 6 for each remove all f,c,a,d,b and for the remaining
# ;     chars that has length 1 (9) that char is g
# ; e = find 8 remove all the other found chars and remaining is e


def find_f(line: str) -> str:
    inputs = line.split(" ")
    count_mapping = {}
    for word in inputs:
        for c in list(word):
            if not c in count_mapping:
                count_mapping[c] = 0
            count_mapping[c] += 1
    return list(filter(lambda x: x[1] == 9, count_mapping.items()))[0][0]


def find_c(line: str, segment_mapping: Dict[str, str]) -> str:
    inputs = line.split(" ")
    one_and_four = list(map(lambda x: x.replace(segment_mapping["f"], ""), filter(
        lambda x: len(x) == 2 or len(x) == 4, inputs)))

    return list(filter(lambda x: len(x) == 1, one_and_four))[0]


# ; a = find 7 and a is whatever char remains besides c & f
def find_a(line: str, segment_mapping: Dict[str, str]) -> str:
    inputs = line.split(" ")
    seven = list(filter(lambda x: len(x) == 3, inputs))[0]
    for val in segment_mapping.values():
        if val == "":
            continue
        seven = seven.replace(val, "")
    return seven


# ; d = find 4 and all length 5 chars and the char they share is d
def find_d(line: str) -> str:
    inputs = line.split(" ")
    length_five = list(filter(lambda x: len(x) == 5, inputs))
    four = list(filter(lambda x: len(x) == 4, inputs))
    count_mapping = {}

    for word in length_five + four:
        for c in list(word):
            if not c in count_mapping:
                count_mapping[c] = 0
            count_mapping[c] += 1

    return list(filter(lambda x: x[1] == (len(length_five) + len(four)), count_mapping.items()))[0][0]


# ; b = find all length 5 and whatever char they don't have in common is b
def find_b(line: str) -> str:
    inputs = line.split(" ")
    fives = list(filter(lambda x: len(x) == 5, inputs))

    count_mapping = {}

    for word in inputs:
        for c in list(word):
            if not c in count_mapping:
                count_mapping[c] = 0
            count_mapping[c] += 1

    return list(filter(lambda x: x[1] == 4, count_mapping.items()))[0][0]


# ; g = find all length 6 for each remove all f,c,a,d,b and for the remaining
# ;     chars that has length 1 (9) that char is g
def find_g(line: str, segment_mapping: Dict[str, str]) -> str:
    inputs = line.split(" ")
    length_six = list(filter(lambda x: len(x) == 6, inputs))

    # print(length_six)
    # print(segment_mapping.values())

    # words = []
    # for word in length_six:
    #     w = word
    #     for val in segment_mapping.values():
    #         if val == "":
    #             continue
    #         w = w.replace(val, "")
    #     words.append(w)

    # return words


def prompt_two(input_lines: List[str]):
    lines = list(map(lambda x: x.split(" | "), input_lines))
    for line in lines:
        segment_mapping = {
            "a": "",
            "b": "",
            "c": "",
            "d": "",
            "e": "",
            "f": "",
            "g": ""
        }
        segment_mapping["f"] = find_f(line[0])
        segment_mapping["c"] = find_c(line[0], segment_mapping)
        segment_mapping["a"] = find_a(line[0], segment_mapping)
        segment_mapping["d"] = find_d(line[0])
        segment_mapping["b"] = find_b(line[0])
        print(find_g(line[0], segment_mapping))


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
