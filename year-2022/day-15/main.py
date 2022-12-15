#! /home/jscott/.pyenv/shims/python

from sys import argv
from typing import List, Tuple
from pprint import pp


# (x, y)
def get_coors(input_lines):
    coors = []
    for line in input_lines:
        formatted_line = line.replace("Sensor at x=", "").replace(
            " y=", "").replace(" closest beacon is at x=", "")

        split_coors = formatted_line.split(":")
        sensor_coor = tuple(
            map(lambda x: int(x), split_coors[0].split(",")))
        beacon_coor = tuple(
            map(lambda x: int(x), split_coors[1].split(",")))

        coors.append((sensor_coor, beacon_coor))

    return coors


def print_map(coor_map, offsets):
    (x_offset, y_offset) = offsets
    digits = len(str(len(coor_map[0])))

    for l in reversed(range(digits)):
        print("     ", end="")
        for k in range(len(coor_map[0])):
            n = k - x_offset
            if n == 0 or n % 5 == 0:
                try:
                    print(list(reversed(str(abs(n))))[l], end="")
                except:
                    print(" ", end="")
            else:
                print(" ", end="")
        print("")

    i = 0
    for line in coor_map:
        print(f'{i - y_offset:04d} {"".join(line)}')
        i += 1


def build_map(coors: List[Tuple[Tuple[str, str]]], padding: int = 10) -> List[List[str]]:
    x_max = float("-inf")
    x_min = float("inf")
    y_max = float("-inf")
    y_min = float("inf")

    coor_map = []

    for coor in coors:
        (sensor, beacon) = coor
        (sensor_x, sensor_y) = sensor
        (beacon_x, beacon_y) = beacon

        if sensor_x > x_max or beacon_x > x_max:
            x_max = sensor_x if sensor_x > beacon_x else beacon_x
        if sensor_y > y_max or beacon_y > y_max:
            y_max = sensor_y if sensor_y > beacon_y else beacon_y

        if sensor_x < x_min or beacon_x < x_min:
            x_min = sensor_x if sensor_x < beacon_x else beacon_x
        if sensor_y < y_min or beacon_y < y_min:
            y_min = sensor_y if sensor_y < beacon_y else beacon_y

    # amount away from 0
    y_offset = abs(y_min) + padding
    x_offset = abs(x_min) + padding

    for i in range(abs(y_max - y_min) + (2 * padding)):
        coor_map.append(
            ["." for k in range(abs(x_max - x_min) + (2 * padding))])

    print((x_max, y_max), (x_min, y_min))

    return coor_map, (x_offset, y_offset)


def calculate_distance(coor):
    (sensor, beacon) = coor
    (sensor_x, sensor_y) = sensor
    (beacon_x, beacon_y) = beacon

    return abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)


def create_area_map(coor_map, coor, offsets, target_pre_offset):
    (sensor, beacon) = coor
    (sensor_x, sensor_y) = sensor
    (beacon_x, beacon_y) = beacon
    (x_offset, y_offset) = offsets
    distance = calculate_distance(coor)
    target = target_pre_offset + y_offset

    # calculate_distance to the target line
    k = abs(distance - abs((sensor_y + y_offset) - target))
    # print(k)
    # print(distance)
    # print(distance - k)

    for i in range(k + 1):
        new_x_down = (sensor_x + x_offset) - i
        new_y_down = (sensor_y + y_offset) + (distance - k)
        new_x_up = (sensor_x + x_offset) - i
        new_y_up = (sensor_y + y_offset) - (distance - k)
        new_x_down_rev = (sensor_x + x_offset) + i
        new_y_down_rev = (sensor_y + y_offset) + (distance - k)
        new_x_up_rev = (sensor_x + x_offset) + i
        new_y_up_rev = (sensor_y + y_offset) - (distance - k)

        existing_symbol_down = coor_map[new_y_down][new_x_down]
        existing_symbol_up = coor_map[new_y_up][new_x_up]
        existing_symbol_down_rev = coor_map[new_y_down_rev][new_x_down_rev]
        existing_symbol_up_rev = coor_map[new_y_up_rev][new_x_up_rev]

        if existing_symbol_down == ".":
            coor_map[new_y_down][new_x_down] = "#"

        if existing_symbol_up == ".":
            coor_map[new_y_up][new_x_up] = "#"

        if existing_symbol_down_rev == ".":
            coor_map[new_y_down_rev][new_x_down_rev] = "#"

        if existing_symbol_up_rev == ".":
            coor_map[new_y_up_rev][new_x_up_rev] = "#"


def place_sensors_and_beacons(coor_map, coors, offsets):
    (x_offset, y_offset) = offsets

    for coor in coors:
        (sensor, beacon) = coor
        (sensor_x, sensor_y) = sensor
        (beacon_x, beacon_y) = beacon

        coor_map[sensor_y + y_offset][sensor_x + x_offset] = "S"
        coor_map[beacon_y + y_offset][beacon_x + x_offset] = "B"


def prompt_one(input_lines: List[str]):
    # target = 10
    target = 2_000_000
    coors = get_coors(input_lines)
    print("building map...")
    (coor_map, offsets) = build_map(coors, 10000)
    print("built map...")
    print("placing beacons...")
    place_sensors_and_beacons(coor_map, coors, offsets)
    print("placed beacons")

    print("adding area maps...")
    for coor in coors:
        create_area_map(coor_map, coor, offsets, target)
    print("added area maps")

    # create_area_map(coor_map, coors[6], offsets, target)

    # count  # in line
    print("counting covered locations...")
    line_to_check = 10 + offsets[1]
    answer = 0
    for i in coor_map[line_to_check]:
        if i == "#":
            answer += 1
    print("done counting")

    # print_map(coor_map, offsets)

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
