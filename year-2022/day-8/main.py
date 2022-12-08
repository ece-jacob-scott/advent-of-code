#! /home/jscott/.pyenv/shims/python

from sys import argv
from typing import List, Set, Tuple, Dict


def searcher(
        tree_line_original: List[int],
        rev: bool,
        found_trees: Set[Tuple[int, int]],
        horizontal: bool,
        counter_axis: int) -> int:
    tree_line = [*tree_line_original]

    if rev:
        tree_line.reverse()

    tallest_tree = -1
    answer = 0
    for i in range(len(tree_line)):
        tree = tree_line[i]

        if not rev:
            axis = i
        else:
            axis = len(tree_line) - 1 - i

        if horizontal:
            coordinates = (axis, counter_axis)
        else:
            coordinates = (counter_axis, axis)

        if tree > tallest_tree:
            if not coordinates in found_trees:
                answer += 1
            tallest_tree = tree
            found_trees.add(coordinates)

    return answer


def prompt_one(input_lines: List[str]):
    # get the columns and
    tree_lines = list(map(lambda x: list(map(int, list(x))), input_lines))

    found_trees = set()
    answer = 0

    for i in range(len(tree_lines)):
        tree_line = tree_lines[i]
        answer += searcher(tree_line, False, found_trees, True, i)
        answer += searcher(tree_line, True, found_trees, True, i)

    # get columns
    columns = []
    for i in range(len(tree_lines[0])):
        columns.append([tree_line[i] for tree_line in tree_lines])

    for i in range(len(columns)):
        tree_line = columns[i]
        answer += searcher(tree_line, False, found_trees, False, i)
        answer += searcher(tree_line, True, found_trees, False, i)

    return answer


def calculate_scenic_score(
        tree_line_original: List[int],
        rev: bool,
        scenic_scores: Dict[Tuple[int, int], int],
        horizontal: bool,
        counter_axis: int):
    tree_line = [*tree_line_original]

    if rev:
        tree_line.reverse()

    tallest_tree = -1
    path = []

    for i in range(len(tree_line)):
        tree = tree_line[i]

        if not rev:
            axis = i
        else:
            axis = len(tree_line) - 1 - i

        if horizontal:
            coordinates = (axis, counter_axis)
        else:
            coordinates = (counter_axis, axis)

        if not coordinates in scenic_scores:
            scenic_scores[coordinates] = 1

        if tree > tallest_tree:
            scenic_scores[coordinates] *= i

            tallest_tree = tree
            path.clear()
            path.append(tree)
        else:
            scenic_score = 1
            # partial back track
            for j in range(len(path)):
                if tree <= path[j]:
                    break
                scenic_score += 1

            scenic_scores[coordinates] *= scenic_score
            path.insert(0, tree)


def prompt_two(input_lines: List[str]):
    tree_lines = list(map(lambda x: list(map(int, list(x))), input_lines))
    scenic_scores = dict()

    for i in range(len(tree_lines)):
        tree_line = tree_lines[i]
        calculate_scenic_score(tree_line, False, scenic_scores, True, i)
        calculate_scenic_score(tree_line, True, scenic_scores, True, i)

    # get columns
    columns = []
    for i in range(len(tree_lines[0])):
        columns.append([tree_line[i] for tree_line in tree_lines])

    for i in range(len(columns)):
        tree_line = columns[i]
        calculate_scenic_score(tree_line, False, scenic_scores, False, i)
        calculate_scenic_score(tree_line, True, scenic_scores, False, i)

    return max(scenic_scores.values())


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
