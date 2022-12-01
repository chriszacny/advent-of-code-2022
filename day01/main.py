"""
Advent of code 2022 Day 1. 

TODO: This is HACKY code. These functions need to be split and a lot of error conditions checked for.

"""

import unittest
import os
import functools


def get_top_three_summed(resultsList: list[int]) -> int:
    return functools.reduce(lambda a, b: a + b, resultsList[0:3])


def get_top_one(resultsList: list[int]) -> int:
    return functools.reduce(lambda a, b: a if a > b else b, resultsList)


def get_each_elf_total_calories_results_sorted_list(rawdata: str) -> int:
    results = []
    data_arr = rawdata.split(os.linesep)
    i = 0
    for _, line in enumerate(data_arr):
        clean_data = line.strip()

        if clean_data == "":
            i += 1
        else:
            int_data = int(line)
            if len(results) < i + 1:
                results.append(int_data)
            else:
                results[i] += int_data
    sortedResults = sorted(results, reverse=True)
    return sortedResults


class TestElfCalorieCalculator(unittest.TestCase):

    def test_basic(self):
        data = """1000
        2000
        3000

        4000

        5000
        6000

        7000
        8000
        9000

        10000
        """
        sortedList = get_each_elf_total_calories_results_sorted_list(data)
        self.assertEqual(get_top_one(sortedList), 24000)
        self.assertEqual(get_top_three_summed(sortedList), 45000)


def main():
    with open("input.dat", "r") as f_hdl:
        str_data = f_hdl.read()
        sortedResults = get_each_elf_total_calories_results_sorted_list(str_data)
        print(get_top_one(sortedResults))
        print(get_top_three_summed(sortedResults))


if __name__ == "__main__":
    main()


#if __name__ == '__main__':
#    unittest.main()
