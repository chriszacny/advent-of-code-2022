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


def calculate_answer(data: "list[str]") -> int:
    """
    2-4,6-8
    """
    answer = 0
    for line in data:
        pairs = line.split(",")
        pair_1_left_number = int(pairs[0].split("-")[0])
        pair_1_right_number = int(pairs[0].split("-")[1])
        pair_2_left_number = int(pairs[1].split("-")[0])
        pair_2_right_number = int(pairs[1].split("-")[1])

        left_tuple = (pair_1_left_number, pair_1_right_number)
        right_tuple = (pair_2_left_number, pair_2_right_number)

        # Calcluate if the left is in the right
        if determine_if_range_contained_in_another_range(left_tuple, right_tuple):
            answer += 1
            continue
        if determine_if_range_contained_in_another_range(right_tuple, left_tuple):
            answer += 1
            continue
    return answer


class TestHarness(unittest.TestCase):

    def test_basic_answer(self):
        data = """2-4,6-8
        2-3,4-5
        5-7,7-9
        2-8,3-7
        6-6,4-6
        2-6,4-8
        """
        lines = sanitize_data(data)
        self.assertEqual(2, calculate_answer(lines))

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
        print(calculate_answer(sanitized_data))
        

if __name__ == "__main__":
    main()


# if __name__ == '__main__':
#    unittest.main()
