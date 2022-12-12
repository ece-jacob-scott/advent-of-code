#! /home/jscott/.pyenv/shims/python

from sys import argv
from typing import List, Tuple
from pprint import pp
import heapq as heap
from collections import defaultdict


# (y, x)
def find_S(grid: List[List[str]]) -> Tuple[int, int]:
    for i in range(len(grid)):
        for k in range(len(grid[i])):
            if grid[i][k] == "S":
                return (i, k)


def create_node(value, coors):
    return {
        "value": value,
        "coors": coors,
        "children": [],
    }


def get_value(grid, coor):
    character = grid[coor[0]][coor[1]]
    if character == "S":
        return ord("a")
    elif character == "E":
        return ord("z")
    return ord(character)


def get_valid_next_moves(
        grid: List[List[str]],
        coor: Tuple[int, int]) -> Tuple[Tuple[int, int]]:
    (y, x) = coor
    value = get_value(grid, coor)
    up = None
    down = None
    left = None
    right = None
    # up
    if not y == 0:
        up = (y - 1, x)
        if 1 < get_value(grid, up) - value:
            up = None
    # down
    if not y == len(grid) - 1:
        down = (y + 1, x)
        if 1 < get_value(grid, down) - value:
            down = None
    # left
    if not x == 0:
        left = (y, x - 1)
        if 1 < get_value(grid, left) - value:
            left = None
    # right
    if not x == len(grid[0]) - 1:
        right = (y, x + 1)
        if 1 < get_value(grid, right) - value:
            right = None

    return (up, down, left, right)


# REWRITE
def create_graph_rec(grid, curr_node, seen, coor):
    value = get_value(grid, coor)
    if value == "E":
        return create_node("E", coor)

    next_moves = get_valid_next_moves(grid, coor)
    next_moves = list(
        filter(lambda x: x != None and not x in seen, next_moves))

    if len(next_moves) == 0:
        return create_node("?", ())

    for move in next_moves:
        node = create_node(grid[move[0]][move[1]], move)

        curr_node["children"].append(node)

        seen.add(move)

        create_graph_rec(grid, node, seen, move)


def create_graph(grid: List[List[str]]):
    start = find_S(grid)
    start_node = create_node("S", start)
    seen = set()
    seen.add(start)

    create_graph_rec(grid, start_node, seen, start)

    return start_node


def traverse_graph(curr_node):
    queue = []
    seen = set()
    dist = defaultdict(lambda: float("inf"))
    pred = defaultdict(lambda: -1)

    seen.add(curr_node["coors"])
    dist[curr_node["coors"]] = 0
    queue.append(curr_node)

    while len(queue) > 0:
        node = queue.pop(0)
        for child in node["children"]:
            if child["coors"] in seen:
                continue
            seen.add(child["coors"])
            dist[child["coors"]] = dist[node["coors"]] + 1
            pred[child["coors"]] = node
            queue.append(child)

            if (child["value"] == "E"):
                return True
    return False


def prompt_one(input_lines: List[str]):
    print(input_lines)
    grid = []
    for line in input_lines:
        grid.append(list(line))

    g = create_graph(grid)

    queue = []
    queue.append(g)

    while len(queue) > 0:
        node = queue.pop(0)
        print(f'node: {node["value"]} {node["coors"]}')

        for child in node["children"]:
            print(f'children: {child["value"]} {child["coors"]}')
            queue.append(child)


def prompt_two(input_lines: List[str]):
    pass


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
