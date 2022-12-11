#! /home/jscott/.pyenv/shims/python

from sys import argv
from typing import List
from math import floor
from pprint import pp
from functools import reduce


def parse_monkey(lines: List[str]):
    monkey = {
        "id": 0,
        "items": [],
        "operation": None,
        "test": None,
        "inspected": 0,
        "divisible_by": 0,
        "true_condition": 0
    }

    # get id
    monkey["id"] = int(lines[0].split(" ")[1].split(":")[0])

    # get starting items
    items = list(
        map(int,
            map(
                lambda x: x.strip(),
                lines[1].split(":")[1].strip().split(","))))

    for item in items:
        monkey["items"].append(item)

    # get operation
    formula_parts = lines[2].split("=")[1].strip().split(" ")

    def create_operation(x, y, operation):
        ops = {
            "*": lambda a, b: a * b,
            "+": lambda a, b: a + b
        }

        if x == "old" and y == "old":
            return lambda a: ops[operation](a, a)

        return lambda a: ops[operation](a, int(y))

    monkey["operation"] = create_operation(
        formula_parts[0],
        formula_parts[2],
        formula_parts[1],
    )

    # get test line
    divisible_by = int(lines[3].split(" ")[-1])
    true_condition = int(lines[4].split(" ")[-1])
    false_condition = int(lines[5].split(" ")[-1])

    monkey["test"] = lambda x: true_condition if x % divisible_by == 0 else false_condition
    monkey["divisible_by"] = divisible_by

    return monkey


def inspect(monkeys, monkey):
    for i in range(len(monkey["items"])):
        worry = monkey["items"].pop(0)

        new_worry = monkey["operation"](worry)

        new_worry = floor(new_worry / 3)

        new_monkey = monkey["test"](new_worry)

        monkeys[new_monkey]["items"].append(new_worry)

        monkey["inspected"] += 1


def prompt_one(input_lines: List[str]):
    monkey_definition = []
    monkeys = []

    for line in input_lines:
        if line == "":
            monkeys.append(parse_monkey(monkey_definition))
            monkey_definition = []
            continue
        monkey_definition.append(line.strip())
    monkeys.append(parse_monkey(monkey_definition))

    rounds = 20
    for i in range(rounds):
        for monkey in monkeys:
            inspect(monkeys, monkey)

    return reduce(
        lambda prev, curr: prev * curr,
        sorted(map(lambda x: x["inspected"], monkeys))[-2:],
        1)


def inspect_two(monkeys, monkey, divisor):
    monkey["items"].sort()
    for i in range(len(monkey["items"])):
        worry = monkey["items"].pop(0)

        new_worry = monkey["operation"](worry)

        new_worry %= divisor

        new_monkey = monkey["test"](new_worry)

        monkeys[new_monkey]["items"].append(new_worry)

        monkey["inspected"] += 1


def prompt_two(input_lines: List[str]):
    monkey_definition = []
    monkeys = []

    for line in input_lines:
        if line == "":
            monkeys.append(parse_monkey(monkey_definition))
            monkey_definition = []
            continue
        monkey_definition.append(line.strip())
    monkeys.append(parse_monkey(monkey_definition))

    rounds = 10000
    divisor = reduce(lambda prev, curr: prev *
                     curr["divisible_by"], monkeys, 1)
    for i in range(rounds):
        for monkey in monkeys:
            inspect_two(monkeys, monkey, divisor)

    return reduce(
        lambda prev, curr: prev * curr,
        sorted(map(lambda x: x["inspected"], monkeys))[-2:],
        1)


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
