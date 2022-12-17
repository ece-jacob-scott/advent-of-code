#! /Users/jxscott/.pyenv/shims/python


######! /home/jscott/.pyenv/shims/python

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

    tunnels[tunnel_name] = {
        "name": tunnel_name,
        "flow_rate": int(flow_rate),
        "children": list(map(lambda x: x.strip(), tunnel_network)),
        "open": False,
    }


def calculate_total_release(flow_rate, time):
    return flow_rate * time


# traverse the tunnels, keep track of the highest amount of flow that can be
# released
def traverse_tunnels(tunnels, start_tunnel, moves=30):
    queue = list()
    # (tunnel_name, parent, total_released, moves_remaining, path_so_far)
    queue.append((start_tunnel, None, 0, moves, [start_tunnel]))
    maximum_release = float("-inf")

    while len(queue) > 0:
        (tunnel_name,
         parent_name,
         total_released,
         moves_remaining,
         path) = queue.pop(0)

        if moves_remaining == 0:
            print(path)
            if total_released > maximum_release:
                maximum_release = total_released
            continue

        curr_tunnel = tunnels[tunnel_name]

        if not curr_tunnel["open"] and curr_tunnel["flow_rate"] != 0:
            # if the current valve isn't open then open it and spend a move
            curr_tunnel["open"] = True
            queue.append((
                tunnel_name,
                None,  # could be good to go to the parent now
                total_released + calculate_total_release(
                    curr_tunnel["flow_rate"], moves_remaining - 1),
                moves_remaining - 1,
                [*path, tunnel_name]))

        # get the moves to each child node and add them to the stack
        for child in curr_tunnel["children"]:
            # it is never more efficient to immediately go back to the parent
            if parent_name and parent_name == child:
                continue
            queue.append((
                child,
                tunnel_name,
                total_released,
                moves_remaining - 1,
                [*path, child]
            ))

    return maximum_release


def foobar(tunnels, start_tunnel, minutes=30):
    queue = []
    queue.append((start_tunnel, 0, minutes))

    while len(queue) > 0:
        (current_tunnel_name, path_flow, remaining_minutes) = queue.pop(0)
        current_tunnel = tunnels[current_tunnel_name]

        # should I take the time to open this valve?
        if not current_tunnel["open"] and current_tunnel["flow_rate"] != 0:
            # open the valve
            current_tunnel["open"] = True
            flow_released = calculate_total_release(
                current_tunnel["flow_rate"], remaining_minutes - 1)
            queue.insert(0, (current_tunnel_name, path_flow +
                         flow_released, remaining_minutes - 1))

        for child in current_tunnel_name["children"]:
            queue.insert(0, (child, remaining_minutes - 1))


def prompt_one(input_lines: List[str]):
    tunnels = defaultdict(lambda: {})
    start_tunnel = "AA"

    # build tunnel system as graph
    # for line in input_lines:
    #     parse_line(line, tunnels)
    tunnels["AA"] = {
        "name": "AA",
        "flow_rate": 0,
        "children": ["BB"],
        "open": False
    }
    tunnels["BB"] = {
        "name": "BB",
        "flow_rate": 10,
        "children": ["AA", "CC"],
        "open": False
    }
    tunnels["CC"] = {
        "name": "CC",
        "flow_rate": 100,
        "children": ["BB"],
        "open": False
    }

    pp(tunnels)

    # traverse graph to find the most efficient way to spend 30 moves
    # answer = traverse_tunnels(tunnels, start_tunnel, 4)

    # return answer


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
