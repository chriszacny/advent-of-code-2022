"""
Advent of code 2022 Day 4. 

TODO: This is HACKY code. These functions need to be split and a lot of error conditions checked for.
"""

import unittest
import string
import os


def sanitize_data(raw_str: str) -> "list[str]":
    lines = raw_str.split(os.linesep)
    return [a.strip() for a in lines if a.strip() != ""]


def determine_if_range_contained_in_another_range(range1: "tuple[int, int]", range2: "tuple[int, int]") -> bool:
    list1 = [a for a in range(range1[0], range1[1] + 1)]
    list2 = [a for a in range(range2[0], range2[1] + 1)]
    for v in list1:
        if v not in list2:
            return False
    return True

def determine_if_any_overlap_in_range(range1: "tuple[int, int]", range2: "tuple[int, int]") -> bool:
    list1 = [a for a in range(range1[0], range1[1] + 1)]
    list2 = [a for a in range(range2[0], range2[1] + 1)]
    for v in list1:
        if v in list2:
            return True
    return False


def get_range_tuples_from_line(line: str) -> "tuple[tuple[int], tuple[int]]":
    pairs = line.split(",")
    pair_1_left_number = int(pairs[0].split("-")[0])
    pair_1_right_number = int(pairs[0].split("-")[1])
    pair_2_left_number = int(pairs[1].split("-")[0])
    pair_2_right_number = int(pairs[1].split("-")[1])

    left_tuple = (pair_1_left_number, pair_1_right_number)
    right_tuple = (pair_2_left_number, pair_2_right_number)
    return (left_tuple, right_tuple)


def calculate_answer_part_one(data: "list[str]") -> int:
    """
    2-4,6-8
    """
    answer = 0
    for line in data:
        ranges = get_range_tuples_from_line(line)

        # Calcluate if the left is in the right
        if determine_if_range_contained_in_another_range(ranges[0], ranges[1]):
            answer += 1
            continue
        if determine_if_range_contained_in_another_range(ranges[1], ranges[0]):
            answer += 1
            continue
    return answer

def calculate_answer_part_two(data: "list[str]") -> int:
    """
    2-4,6-8
    """
    answer = 0
    for line in data:
        ranges = get_range_tuples_from_line(line)

        # Calcluate if the left is in the right
        if determine_if_any_overlap_in_range(ranges[0], ranges[1]):
            answer += 1
            continue
        if determine_if_any_overlap_in_range(ranges[1], ranges[0]):
            answer += 1
            continue
    return answer


class TestHarness(unittest.TestCase):

    def test_basic_answer_part_one(self):
        data = """2-4,6-8
        2-3,4-5
        5-7,7-9
        2-8,3-7
        6-6,4-6
        2-6,4-8
        """
        lines = sanitize_data(data)
        self.assertEqual(2, calculate_answer_part_one(lines))

    def test_basic_answer_part_two(self):
        data = """2-4,6-8
        2-3,4-5
        5-7,7-9
        2-8,3-7
        6-6,4-6
        2-6,4-8
        """
        lines = sanitize_data(data)
        self.assertEqual(4, calculate_answer_part_two(lines))

    def test_determine_if_range_contained_in_another_range(self):
        r1 = (2, 4)
        r2 = (4, 5) # False
        self.assertEqual(determine_if_range_contained_in_another_range(r1, r2), False)

        r3 = (1, 2)
        r4 = (1, 5) # True
        self.assertEqual(determine_if_range_contained_in_another_range(r3, r4), True)

        r5 = (1, 1)
        r6 = (1, 1) # True
        self.assertEqual(determine_if_range_contained_in_another_range(r5, r6), True)


def main():
    with open("input.dat", "r") as f_hdl:
        str_data = f_hdl.read()
        sanitized_data = sanitize_data(str_data)
        print(calculate_answer_part_two(sanitized_data))
        

if __name__ == "__main__":
    main()


# if __name__ == '__main__':
#    unittest.main()
