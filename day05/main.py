"""
Advent of code 2022 Day 5. 

TODO: This is HACKY code. These functions need to be split and a lot of error conditions checked for.
"""

import unittest
import os
import sys

"""
Line lengths:
1 crate = 3 (c*3 + 0)
2 crate = 7 (c*3 + 1)
3 create = 11 (c*3 + 2)
4 crate = 15 (c*3 + 3)
"""


class Stack:
    def __init__(self):
        self.data = []
    
    def push(self, data: str):
        self.data.insert(0, data)

    def pop(self) -> str:
        return self.data.pop(0)

    def append_bottom(self, data: str):
        """
        This builds the stack "backwards", acting as a queue. We do this because of the way the input is given to us.
        """
        self.data.append(data)

    def __str__(self) -> str:
        to_return = ""
        for v in self.data:
            to_return += '['
            to_return += v
            to_return += ']'
            to_return += os.linesep
        return to_return

    def __repr__(self) -> str:
        return self.__str__()


def get_count_of_stacks(bottom_line: str ) -> int:
    count = 0
    for c in bottom_line:
        if c == '[':
            count += 1
    return count


def build_stacks(stacks_input_data: str) -> list[Stack]:
    lines = stacks_input_data.split(os.linesep)
    count_of_stacks = get_count_of_stacks(lines[len(lines)-1]) # take the bottom line as that should have all stacks (assuming we don't allow starting with empty stacks)
    #expected_line_length = (count_of_stacks * 3) + (count_of_stacks - 1)
    # This could also probably be done via a RexEx match
    stacks = [Stack() for _ in range(0, count_of_stacks)]
    for line in lines:
        if line.strip() == "":
            continue
        for i in range(0, count_of_stacks):
            stack_data_line_pos = (i * 4) + 1 # 1, 5, 9, 13, ...
            if line[stack_data_line_pos].strip() != "":
                stacks[i].append_bottom(line[stack_data_line_pos])
    # for s in stacks:
    #    print(s)
    return stacks


def parse_instruction_line(line: str) -> tuple[int, int, int]:
    """
    Return (count to move, the from stack, the target stack)
    """
    line_list = line.split(" ")
    return int(line_list[1]), int(line_list[3]), int(line_list[5])


def build_instructions(instructions_input_data: str) -> list[tuple[int,int,int]]:
    to_return = []
    lines = instructions_input_data.split(os.linesep)
    for line in lines:
        if line.strip() == "":
            continue
        to_return.append(parse_instruction_line(line))
    return to_return


def move_stacks_and_return_top_of_each_stack(stacks_input_data: str, instructions_input_data: str) -> str:
    #print(f"input data: {stacks_input_data}")
    to_return = ""
    stacks = build_stacks(stacks_input_data)
    instructions = build_instructions(instructions_input_data)
    for _, v in enumerate(instructions):
        count_of_crates_to_move = v[0]
        stack_to_move_crates_from = v[1]
        stack_to_move_crates_to = v[2]
        #print(f"STACKS: {stacks}")
        #print(f"Move {count_of_crates_to_move} crates from stack {v[1]} to stack {v[2]}")
        temp_list = []
        for i in range(0, count_of_crates_to_move):
            temp_list.insert(0, stacks[stack_to_move_crates_from - 1].pop())
        for c in temp_list:
            stacks[stack_to_move_crates_to - 1].push(c)
    for stack in stacks:
        to_return += stack.pop()
    return to_return


class TestHarness(unittest.TestCase):

    def test_get_count_of_stacks(self):
        r = get_count_of_stacks("[Z] [M] [P]")
        self.assertEqual(3, r)

    def test_stack(self):
        s = Stack()
        s.push('a')
        s.push('b')
        self.assertEqual(s.pop(), 'b')
        self.assertEqual(s.pop(), 'a')

    def test_build_stacks(self):
        stacks_input_data = """
    [D]    
[N] [C]    
[Z] [M] [P]"""
        stacks = build_stacks(stacks_input_data)
        self.assertEqual(len(stacks), 3)

    def test_move_parser(self):
        line = "move 2 from 2 to 8"
        val = parse_instruction_line(line)
        self.assertEqual(val[0], 2)
        self.assertEqual(val[1], 2)
        self.assertEqual(val[2], 8)
    
    def test_move_stacks_and_return_top_of_each_stack(self):
        stacks_input_data = """
    [D]    
[N] [C]    
[Z] [M] [P]"""
        instructions_input_data = """
move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
        """
        answer = move_stacks_and_return_top_of_each_stack(stacks_input_data, instructions_input_data)
        self.assertEqual("MCD", answer)

def main():
    with open("stacks.dat", "r") as f_hdl_stacks:
        stacks_str_data = f_hdl_stacks.read()
        with open("move_instructions.dat", "r") as f_hdl_move_instructions:
            move_instructions_str_data = f_hdl_move_instructions.read()
            answer = move_stacks_and_return_top_of_each_stack(stacks_str_data, move_instructions_str_data)
            print(answer)
        

if __name__ == "__main__":
    main()


# if __name__ == '__main__':
#    unittest.main()
