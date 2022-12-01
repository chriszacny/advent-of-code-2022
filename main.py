import unittest
import os
import functools


def get_total_calories_from_elf_with_most_calories(rawdata: str) -> int:
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
    toReturn = functools.reduce(lambda a, b: a if a > b else b, results)
    return toReturn


class TestElfCalorieCalculator(unittest.TestCase):

    def test_basic(self):
        data = """1000
        2000
        3000

        5000

        4000
        """
        self.assertEqual(get_total_calories_from_elf_with_most_calories(data), 6000)


def main():
    with open("input.dat", "r") as f_hdl:
        str_data = f_hdl.read()
        print(get_total_calories_from_elf_with_most_calories(str_data))


if __name__ == "__main__":
    main()


#if __name__ == '__main__':
#    unittest.main()
