#! /home/jscott/.pyenv/shims/python

from sys import argv
from typing import List, Tuple
from pprint import pp
from collections import defaultdict


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


def calculate_distance(coor):
    (sensor, beacon) = coor
    (sensor_x, sensor_y) = sensor
    (beacon_x, beacon_y) = beacon

    return abs(sensor_x - beacon_x) + abs(sensor_y - beacon_y)


def create_area_map(coor, existing_symbols, target_line, target):
    (sensor, beacon) = coor
    (sensor_x, sensor_y) = sensor
    (beacon_x, beacon_y) = beacon
    distance = calculate_distance(coor)

    # calculate_distance to the target line
    k = abs(distance - abs(sensor_y - target))

    for i in range(k + 1):
        new_x_down = sensor_x - i
        new_y_down = sensor_y + (distance - k)
        new_x_up = sensor_x - i
        new_y_up = sensor_y - (distance - k)
        new_x_down_rev = (sensor_x) + i
        new_y_down_rev = sensor_y + (distance - k)
        new_x_up_rev = sensor_x + i
        new_y_up_rev = sensor_y - (distance - k)

        up_left = (new_x_up, new_y_up)
        down_left = (new_x_down, new_y_down)
        up_right = (new_x_up_rev, new_y_up_rev)
        down_right = (new_x_down_rev, new_y_down_rev)

        if new_y_up == target and (not up_left in existing_symbols):
            target_line.add(up_left)

        if new_y_down == target and (not down_left in existing_symbols):
            target_line.add(down_left)

        if new_y_up_rev == target and (not up_right in existing_symbols):
            target_line.add(up_right)

        if new_y_down_rev == target and (not down_right in existing_symbols):
            target_line.add(down_right)

    return target_line


def prompt_one(input_lines: List[str]):
    # target = 10
    target = 2_000_000
    coors = get_coors(input_lines)
    sensors_and_beacons = set()

    for coor in coors:
        (sensor, beacon) = coor
        sensors_and_beacons.add(sensor)
        sensors_and_beacons.add(beacon)

    target_line = set()
    for coor in coors:
        create_area_map(coor, sensors_and_beacons, target_line, target)

    return len(target_line)


def get_perimeter_coors(start: Tuple[int, int], distance: int, clamp: int, test_coors: set):
    (x, y) = start

    for i in range(distance):
        # for each iteration get the point right out side of the range
        left_down = (((x - distance) + i) - 1, (y + i))
        right_down = (((x + distance) - i) + 1, (y + i))
        left_up = (((x - distance) + i) - 1, (y - i))
        right_up = (((x + distance) - i) + 1, (y - i))

        x_min = left_down[0]
        x_max = right_down[0]
        y_min = left_up[1]
        y_max = left_down[1]

        if x_min < 0 or y_min < 0:
            continue
        if x_max > clamp or y_max > clamp:
            continue

        test_coors.add(left_down)
        test_coors.add(left_up)
        test_coors.add(right_down)
        test_coors.add(right_up)


def prompt_two(input_lines: List[str]):
    # O(1) operations: calculating distance, calculating area of sensor
    # O(S) comparing a point to all sensors distances
    # can't loop through array of coordinates with an area of (4_000_000 * 4_000_000)
    coors = get_coors(input_lines)
    # clamp = 20
    clamp = 4_000_000
    beacon_coor = None

    detection_distances = defaultdict(lambda: 0)
    test_coors = set()

    print("getting possible locations...")

    for coor in coors:
        distance = calculate_distance(coor)
        detection_distances[coor] = (coor[0], distance)
        get_perimeter_coors(coor[0], distance, clamp, test_coors)

    print("getting beacon coor...")

    for possible_location in test_coors:
        tracker = 0
        for sensor in detection_distances.values():
            (coor, distance) = sensor
            if calculate_distance((coor, possible_location)) <= distance:
                break
            tracker += 1
        if tracker == len(detection_distances.values()):
            beacon_coor = possible_location
            break

    if beacon_coor is None:
        print("didn't find a beacon")
        return

    return (beacon_coor[0] * 4_000_000) + beacon_coor[1]


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
