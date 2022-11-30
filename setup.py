#! /home/jscott/.pyenv/shims/python
from sys import argv
from os import getcwd, makedirs, path, system

valid_year = ["2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022"]
valid_day = [
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "11",
    "12",
    "13",
    "14",
    "15",
    "16",
    "17",
    "18",
    "19",
    "20",
    "21",
    "22",
    "23",
    "24",
    "25"
]
main_source = """#! /home/jscott/.pyenv/shims/python

from sys import argv
from typing import List


def prompt_one(input_lines: List[str]):
    pass


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
"""

if __name__ == "__main__":
    if len(argv) != 3:
        print("use like './setup.py {year} {day}'")
        exit(1)

    [program_name, year, day] = argv

    if year not in valid_year:
        print(f'year must be one of {valid_year}')
        exit(1)

    if day not in valid_day:
        print(f'day must be one of {valid_day}')
        exit(1)

    current_directory = getcwd()

    if "year" not in current_directory.split("/")[-1]:
        # make this smart enough to create the year directory or at least read
        # the year to take away one of the arguments required
        print("current directory is not a year directory please create one")
        exit(1)

    # create a new directory if none exists
    new_day_directory = f'{current_directory}/day-{day}'

    if not path.exists(new_day_directory):
        print(f'creating {new_day_directory}')
        makedirs(new_day_directory)
    else:
        print(f'already created {new_day_directory}')

    # create file called main.py
    if not path.exists(new_day_directory + "/main.py"):
        print("creating main.py...")
        with open(new_day_directory + "/main.py", "w+") as f:
            f.write(main_source)
        system(f'chmod +x {new_day_directory + "/main.py"}')
    else:
        print("already created main.py")

    if not path.exists(new_day_directory + "/input-1.txt"):
        print("downloading input-1.txt")
        system(
            f'wget --load-cookies={current_directory}/../adventofcode.com_cookies.txt https://adventofcode.com/{year}/day/{day}/input -O {new_day_directory}/input-1.txt')
    else:
        print("already downloaded input-1.txt")
