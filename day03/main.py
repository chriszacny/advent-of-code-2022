"""
Advent of code 2022 Day 3. 

TODO: This is HACKY code. These functions need to be split and a lot of error conditions checked for.

"""

import unittest
import string
import os


def get_priority_table() -> "dict[str, int]":
    lowercase = list(string.ascii_lowercase)
    uppercase = list(string.ascii_uppercase)
    priority_table = {}
    for i, v in enumerate(lowercase):
        priority_table[v] = i + 1
    for i, v in enumerate(uppercase):
        priority_table[v] = i + 27
    return priority_table


def get_compartments_data(data: str) -> "tuple[str, str]":
    return (data[:int(len(data) / 2)], data[int(len(data) / 2):])


def find_duplicate(str1: str, str2: str) -> str:
    set1 = set(str1)
    set2 = set(str2)
    result = set1.intersection(set2)
    return list(result)[0]


def find_sum_of_all_duplicates(rawdata: str) -> int:
    current_sum = 0
    lines = rawdata.split(os.linesep)
    for line in lines:
        sanitzed = line.strip()
        if sanitzed == "":
            continue
        compartments = get_compartments_data(sanitzed)
        dup = find_duplicate(compartments[0], compartments[1])
        current_sum += int(get_priority_table()[dup])
    return current_sum


def sanitize_data(raw_str: str) -> "list[str]":
    lines = raw_str.split(os.linesep)
    return [a.strip() for a in lines if a.strip() != ""]


def build_groups_of_three(lines: "list[str]") -> "list[list[set]]":
    groups = []
    cur_set_list = None
    for i, line in enumerate(lines):
        if i % 3 == 0:
            # start a new group
            groups.append([])
            if cur_set_list is None:
                cur_set_list = 0
            else:
                cur_set_list += 1
        groups[cur_set_list].append(set(line))
    return groups


def get_elf_badge_int_value_from_group(group: "list[set]") -> int:
    common_value = list(group[0].intersection(group[1]).intersection(group[2]))[0]
    return int(get_priority_table()[common_value])


def find_sum_of_elf_group_common_badges(rawdata: str) -> int:
    current_sum = 0
    lines = sanitize_data(rawdata)
    groups = build_groups_of_three(lines)
    for group in groups:
        current_sum += get_elf_badge_int_value_from_group(group)
    return current_sum
    

class TestHarness(unittest.TestCase):

    def test_get_compartments_data(self):
        self.assertEqual(get_compartments_data("vJrwpWtwJgWrhcsFMMfFFhFp"), ("vJrwpWtwJgWr", "hcsFMMfFFhFp"))

    def test_priority_table(self):
        t = get_priority_table()
        self.assertEqual(t["a"], 1)
        self.assertEqual(t["A"], 27)
        self.assertEqual(t["Z"], 52)

    def test_find_duplicate(self):
        result = find_duplicate("asPd", "qEzP")
        self.assertEqual("P", result)

    def test_find_sum_of_all_duplicates(self):
        data = """vJrwpWtwJgWrhcsFMMfFFhFp
        jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
        PmmdzqPrVvPwwTWBwg
        wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
        ttgJtRGJQctTZtZT
        CrZsJsPPZsGzwwsLwLmpwMDw
        """
        result = find_sum_of_all_duplicates(data)
        self.assertEqual(result, 157)

    def test_build_groups_of_three(self):
        data = """vJrwpWtwJgWrhcsFMMfFFhFp
        jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
        PmmdzqPrVvPwwTWBwg
        wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
        ttgJtRGJQctTZtZT
        CrZsJsPPZsGzwwsLwLmpwMDw
        """
        lines = sanitize_data(data)
        groups = build_groups_of_three(lines)
        self.assertEqual(len(groups), 2)
    
    def test_find_sum_of_elf_group_common_badges(self):
        data = """vJrwpWtwJgWrhcsFMMfFFhFp
        jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
        PmmdzqPrVvPwwTWBwg
        wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
        ttgJtRGJQctTZtZT
        CrZsJsPPZsGzwwsLwLmpwMDw
        """
        result = find_sum_of_elf_group_common_badges(data)
        self.assertEqual(result, 70)


def main():
    with open("input.dat", "r") as f_hdl:
        str_data = f_hdl.read()
        #print(find_sum_of_all_duplicates(str_data))
        print(find_sum_of_elf_group_common_badges(str_data))
        

if __name__ == "__main__":
    main()


# if __name__ == '__main__':
#    unittest.main()
