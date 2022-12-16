#! /home/jscott/.pyenv/shims/python

from sys import argv
from typing import List
from collections import defaultdict
from pprint import pp


def parse_line(line: str, tunnels):
    clean_line = line.replace("Valve ", "").replace(" has flow rate=", ",").replace(
        "; tunnel leads to valve ", ","
    ).replace(
        "; tunnels lead to valves ", ","
    )

    (tunnel_name, flow_rate, *tunnel_network) = clean_line.split(",")

    # print((tunnel_name, flow_rate, tunnel_network))

    tunnels[tunnel_name] = {
        "name": tunnel_name,
        "flow_rate": int(flow_rate),
        "children": list(map(lambda x: x.strip(), tunnel_network)),
        "open": False
    }


def calculate_total_release(flow_rate, time):
    return flow_rate * time


def traverse_tunnels(tunnels, start_tunnel, moves=30):
    remaining_moves = moves
    queue = list()
    queue.append(start_tunnel)
    total_release = 0

    while len(queue) > 0 and remaining_moves != 0:
        curr_tunnel = tunnels[queue.pop(0)]
        print(f'move {remaining_moves} valve {curr_tunnel["name"]}')

        # how much pressure to spend on move opening the valve
        open_current_release = 0
        if curr_tunnel["open"]:
            open_current_release = 0
        else:
            open_current_release = calculate_total_release(
                curr_tunnel["flow_rate"], remaining_moves - 1)

        child_releases = []
        for child in curr_tunnel["children"]:
            child_tunnel = tunnels[child]
            if child_tunnel["open"]:
                child_releases.append((child, 0))
                continue
            child_releases.append((child, calculate_total_release(
                tunnels[child]["flow_rate"],
                remaining_moves - 2
            )))

        max_child_release = max(child_releases, key=lambda x: x[1])

        # print(max_child_release, open_current_release)

        # if we get more value in a child valve then go to that one and
        # open it skipping this one, this costs a move
        if max_child_release[1] > open_current_release:
            queue.append(max_child_release[0])
            remaining_moves -= 1
        else:
            # else open the current valve
            curr_tunnel["open"] = True
            queue.append(curr_tunnel["name"])
            total_release += open_current_release
            remaining_moves -= 1

    if remaining_moves < 30:
        print("did not use all 30 moves")

    return total_release


def prompt_one(input_lines: List[str]):
    tunnels = defaultdict(lambda: {})
    start_tunnel = "AA"

    # build tunnel system as graph
    for line in input_lines:
        parse_line(line, tunnels)

    # pp(tunnels)

    # traverse graph to find the most efficient way to spend 30 moves
    answer = traverse_tunnels(tunnels, start_tunnel)

    return answer


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
