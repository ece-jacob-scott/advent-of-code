#! /home/jscott/.pyenv/shims/python

from sys import argv
from typing import List
from pprint import pp
from collections import defaultdict


# (y, x)
def find_S(grid):

    for i in range(len(grid)):
        for k in range(len(grid[i])):
            if grid[i][k] == "S":
                return (i, k)


def find_E(grid):
    for i in range(len(grid)):
        for k in range(len(grid[i])):
            if grid[i][k] == "E":
                return (i, k)


def get_value(grid, coor):
    (y, x) = coor

    max_y = len(grid)
    max_x = len(grid[0])

    if y < 0 or y == max_y or x < 0 or x == max_x:
        return None

    character = grid[y][x]

    if character == "E":
        return ord("z")
    if character == "S":
        return ord("a")
    return ord(character)


def get_valid_next_move(grid, curr_coor):
    moves = []
    (y, x) = curr_coor
    curr_value = get_value(grid, curr_coor)
    up = (y - 1, x)
    up = (get_value(grid, up), up)
    down = (y + 1, x)
    down = (get_value(grid, down), down)
    left = (y, x - 1)
    left = (get_value(grid, left), left)
    right = (y, x + 1)
    right = (get_value(grid, right), right)
    for move in [up, down, left, right]:
        if move[0] and (move[0] - curr_value) <= 1:
            moves.append(move[1])
    return tuple(filter(lambda x: not x == None, moves))


def bfs_path_finding(grid, start_coor):
    queue = []
    queue.append(start_coor)
    seen = set()
    distance = defaultdict(lambda: float("inf"))
    distance[start_coor] = 0

    while len(queue) > 0:
        curr_coor = queue.pop(0)
        seen.add(curr_coor)

        children = get_valid_next_move(grid, curr_coor)
        for child in children:
            if child in seen:
                continue
            old_cost = distance[child]
            new_cost = distance[curr_coor] + 1
            if new_cost < old_cost:
                queue.append(child)
                distance[child] = new_cost

    return distance


def prompt_one(input_lines: List[str]):
    grid = []
    for i in range(len(input_lines)):
        row = []
        for k in range(len(input_lines[i])):
            row.append(input_lines[i][k])
        grid.append(row)
    return bfs_path_finding(grid, find_S(grid))[find_E(grid)]


def find_all_starting_coors(grid):
    starting_coors = []
    for i in range(len(grid)):
        for k in range(len(grid[i])):
            if grid[i][k] == "a" or grid[i][k] == "S":
                starting_coors.append((i, k))
    return starting_coors


def prompt_two(input_lines: List[str]):
    grid = []
    for i in range(len(input_lines)):
        row = []
        for k in range(len(input_lines[i])):
            row.append(input_lines[i][k])
        grid.append(row)
    starts = find_all_starting_coors(grid)
    ending_coors = find_E(grid)
    curr_distance = float("inf")
    for start in starts:
        # run path finding on all starts
        distance = bfs_path_finding(grid, start)[ending_coors]
        if distance < curr_distance:
            curr_distance = distance
    return curr_distance


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
