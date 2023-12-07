#! /home/jscott/.pyenv/shims/python

from sys import argv
from typing import List, Dict
from dataclasses import dataclass
from collections import defaultdict
from functools import cmp_to_key
from pprint import pprint


hand_type_to_strength = {
    "five_of_a_kind": 7,
    "four_of_a_kind": 6,
    "full_house": 5,
    "three_of_a_kind": 4,
    "two_pair": 3,
    "one_pair": 2,
    "high_card": 1,
}

card_to_strength = {
    "A": 12,
    "K": 11,
    "Q": 10,
    "J": 9,
    "T": 8,
    "9": 7,
    "8": 6,
    "7": 5,
    "6": 4,
    "5": 3,
    "4": 2,
    "3": 1,
    "2": 0,
}


@dataclass
class Hand:
    hand: str
    bid: str
    strength: int = -1

    def is_better(self, hand: "Hand") -> bool:
        if self.get_strength() != hand.get_strength():
            return self.get_strength() > hand.get_strength()

        i = 0
        while i < len(self.hand):
            if card_to_strength[self.hand[i]] != card_to_strength[hand.hand[i]]:
                return card_to_strength[self.hand[i]] > card_to_strength[hand.hand[i]]

            i += 1

        raise Exception("hands are the same is this allowed?")

    def is_better_two(self, hand: "Hand") -> bool:
        if self.get_strength_two() != hand.get_strength_two():
            return self.get_strength_two() > hand.get_strength_two()

        i = 0
        while i < len(self.hand):
            if card_to_strength[self.hand[i]] != card_to_strength[hand.hand[i]]:
                return card_to_strength[self.hand[i]] > card_to_strength[hand.hand[i]]

            i += 1

        raise Exception("hands are the same is this allowed?")

    @staticmethod
    def calculate_strength(hand: "Hand") -> int:
        strength = 0
        m = defaultdict(lambda: 0)

        for c in hand.hand:
            m[c] += 1

        values = m.values()

        # if the only value is 5 then it's five_of_a_kind
        if len(values) == 1 and 5 in values:
            strength = hand_type_to_strength["five_of_a_kind"]
        elif len(values) == 2 and 4 in values:
            strength = hand_type_to_strength["four_of_a_kind"]
        elif len(values) == 2 and 3 in values and 2 in values:
            strength = hand_type_to_strength["full_house"]
        elif len(values) == 3 and 3 in values:
            strength = hand_type_to_strength["three_of_a_kind"]
        elif len(values) == 3 and 2 in values:
            strength = hand_type_to_strength["two_pair"]
        elif len(values) == 4 and 2 in values:
            strength = hand_type_to_strength["one_pair"]
        elif len(values) == 5:
            strength = hand_type_to_strength["high_card"]

        return strength

    def get_strength(self):
        if self.strength != -1:
            return self.strength

        self.strength = Hand.calculate_strength(self)

        return self.strength

    def get_strength_two(self):
        # check if a J is in the hand
        if "J" not in self.hand:
            return self.get_strength()

        if self.strength != -1:
            return self.strength

        strength = -1
        m = defaultdict(lambda: 0)

        for c in self.hand:
            m[c] += 1

        values = m.values()

        # if the only value is 5 then it's five_of_a_kind
        if len(values) == 1 and 5 in values:
            strength = hand_type_to_strength["five_of_a_kind"]
        if len(values) == 2 and 4 in values:
            # if there are 4 of a kind and the last one is a jack then the best hand is 5 of a kind
            strength = hand_type_to_strength["five_of_a_kind"]
        elif len(values) == 2 and 3 in values and 2 in values:
            # if there is a full house then 2 or 3 are jacks and then it can be 5 of a kind
            strength = hand_type_to_strength["five_of_a_kind"]
        elif len(values) == 3 and 3 in values:
            if m["J"] == 3:
                # if the jacks are the 3 of a kind then you can make a 4 of a kind hand
                strength = hand_type_to_strength["four_of_a_kind"]
            else:
                # if the jack is one of the odd ones then you can make a 4 of a kind hand
                strength = hand_type_to_strength["four_of_a_kind"]
        elif len(values) == 3 and 2 in values:
            if m["J"] == 2:
                # match with the other pair to make four of a kind
                strength = hand_type_to_strength["four_of_a_kind"]
            else:
                # match with a pair to get a full house
                strength = hand_type_to_strength["full_house"]
        elif len(values) == 4 and 2 in values:
            strength = hand_type_to_strength["three_of_a_kind"]
        elif len(values) == 5:
            strength = hand_type_to_strength["one_pair"]

        self.strength = strength
        return strength


def parse_hand(line: str):
    hand_str, bid_str = line.split(" ")

    return Hand(hand_str, int(bid_str))


def prompt_one(input_lines: List[str]):
    answer = 0
    hands: List[Hand] = []

    for line in input_lines:
        hands.append(parse_hand(line))

    def compare(hand_one: Hand, hand_two: Hand) -> int:
        return 1 if hand_one.is_better(hand_two) else -1

    for i, h in enumerate(sorted(hands, key=cmp_to_key(compare))):
        answer += h.bid * (i + 1)

    return answer


def prompt_two(input_lines: List[str]):
    global card_to_strength
    # for the J is lowest card rule
    card_to_strength["J"] = -1

    answer = 0
    hands: List[Hand] = []

    for line in input_lines:
        hands.append(parse_hand(line))

    def compare(hand_one: Hand, hand_two: Hand) -> int:
        return 1 if hand_one.is_better_two(hand_two) else -1

    for i, h in enumerate(sorted(hands, key=cmp_to_key(compare))):
        answer += h.bid * (i + 1)

    return answer


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

    with open(problem_input, "r") as f:
        input_lines = [line.rstrip() for line in f]

    if problem == "1":
        print(prompt_one(input_lines))
    else:
        print(prompt_two(input_lines))
