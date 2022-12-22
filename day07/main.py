"""
Advent of code 2022 Day 7. 

TODO: This is HACKY code. These functions need to be split and a lot of error conditions checked for.
In addition this code breaks a lot of rules of functional programming (lots of side effects and mutable data)
probably because I went with more of a class-based approach for this one.

"""

import unittest
import os
from enum import Enum
from abc import ABC, abstractmethod


TOTAL_FS_DISK_SPACE=70000000
UPDATE_SPACE_REQUIRED=30000000


class NodeType(Enum):
    File = 1
    Directory = 2


class FilesystemCommand(Enum):
    cd = 1
    ls = 2


class Node:
    def __init__(self):
        self.children = None
        self.parent = None
        self.type = None
        self.size = 0
        self.name = ""

    def __str__(self):
        data = {}
        if self.children is not None:
            data["children"] = [ str(x) for x in self.children ]
        data["parent"] = self.parent
        data["type"] = self.type
        data["size"] = self.size
        data["name"] = self.name
        return str(data)


class Filesystem:
    def __init__(self):
        self.root = Node()
        self.root.type = NodeType.Directory
        self.root.name = "/"
        self.root.children = []
        self.current_node = None
        self.answer_one = 0
        self.answer_two = 0
    
    def change_directory(self, directory: str) -> None:
        return None

    def calculate_directory_size(self, cur_node):
        if len([x for x in cur_node.children if x.type == NodeType.Directory]) == 0:
            cur_node.size = sum([x.size for x in cur_node.children])
        else:
            for directory in [x for x in cur_node.children if x.type == NodeType.Directory]:
                self.calculate_directory_size(directory)
            cur_node.size = sum([x.size for x in cur_node.children])

    def calculate_answer_one(self, cur_node):
        if cur_node.size <= 100000:
            #print(cur_node.name)
            self.answer_one += cur_node.size
        for directory in [x for x in cur_node.children if x.type == NodeType.Directory]:
            #if directory.size <= 100000:
            #print(directory.name)
            self.calculate_answer_one(directory)
    
    def find_closest_to_number(self, cur_dir, space_needed_to_free_up):
        for directory in [x for x in cur_dir.children if x.type == NodeType.Directory]:
            self.find_closest_to_number(directory, space_needed_to_free_up)
        # compare current_answer to current dir size
        if cur_dir.size >= space_needed_to_free_up and (cur_dir.size < self.answer_two or self.answer_two == 0):
            self.answer_two = cur_dir.size

    def calculate_answer_two(self):
        total_used_space = self.root.size
        unused_space = TOTAL_FS_DISK_SPACE - total_used_space
        if unused_space >= UPDATE_SPACE_REQUIRED:
            return 0
        space_needed_to_free_up = UPDATE_SPACE_REQUIRED - unused_space
        self.find_closest_to_number(self.root, space_needed_to_free_up)

    def __str__(self):
        return str(self.root)


class ParsedDataType(Enum):
    Input = 1
    Output = 2


class ParsedDataLine(ABC):
    def __init__(self, type_of_data: ParsedDataType):
        self.type_of_data = type_of_data

    @abstractmethod
    def execute(self, filesystem: Filesystem):
        pass


class Output(ParsedDataLine):
    def __init__(self, type_of_data: ParsedDataType, output: "list[str]"):
        super().__init__(type_of_data)
        self.output = output

    def execute(self, filesystem: Filesystem):
        new_node = Node()
        new_node.name = self.output[1]
        if self.output[0] == "dir":
            new_node.type = NodeType.Directory
            new_node.children = []
        else:
            new_node.type = NodeType.File
            new_node.size = int(self.output[0])
        new_node.parent = filesystem.current_node
        filesystem.current_node.children.append(new_node)


class Command(ParsedDataLine):
    def __init__(self, type_of_data: ParsedDataType, command: str, argument: str = None):
        super().__init__(type_of_data)
        self.command = FilesystemCommand[command]
        self.argument = argument

    def execute(self, filesystem: Filesystem):
        if self.command == FilesystemCommand.cd:
            if self.argument == "/":
                filesystem.current_node = filesystem.root
            elif self.argument == "..":
                # go up to the parent
                filesystem.current_node = filesystem.current_node.parent
            else:
                # assuming an ls was done:
                new_node = list(filter(lambda x: x.name == self.argument, filesystem.current_node.children))[0]
                filesystem.current_node = new_node
        elif self.command == FilesystemCommand.ls:
            pass


def filesystem_factory(lines: "list[ParsedDataLine]") -> Filesystem():
    filesystem = Filesystem()
    for i, parsed_data_line in enumerate(lines):
        parsed_data_line.execute(filesystem)
    return filesystem


def sanitize_data(raw_str: str) -> "list[str]":
    lines = raw_str.split(os.linesep)
    return [a.strip() for a in lines if a.strip() != ""]


def parse_input_data(lines: "list[str]") -> "list[ParsedDataLine]":
    to_return = []
    for line in lines:
        split_data = line.split(" ")
        if split_data[0] == "$":
            command = Command(ParsedDataType.Input, split_data[1])
            if len(split_data) == 3:
                command.argument = split_data[2]
            to_return.append(command)
        else:
            output = Output(ParsedDataType.Output, split_data)
            to_return.append(output)
    return to_return


class TestHarness(unittest.TestCase):

    def test_basic(self):
        basic_script = """
        $ cd /
        $ ls
        dir a
        14848514 b.txt
        8504156 c.dat
        dir d
        $ cd a
        $ ls
        8504 m.dat
        """
        lines = sanitize_data(basic_script)
        parsed_lines = parse_input_data(lines)
        self.assertIsInstance(parsed_lines[0], Command)
        self.assertIsInstance(parsed_lines[1], Command)
        self.assertIsInstance(parsed_lines[2], Output)

        a_filesystem = filesystem_factory(parsed_lines)
        self.assertIsInstance(a_filesystem, Filesystem)
        self.assertEqual(a_filesystem.root.name, "/")
        self.assertEqual(len(a_filesystem.root.children), 4)
        #print(a_filesystem)
        a_filesystem.calculate_directory_size(a_filesystem.root)
        self.assertEqual(a_filesystem.root.size, 23361174)
        a_filesystem.calculate_answer_one(a_filesystem.root)
        self.assertEqual(a_filesystem.answer_one, 8504)

    def test_full(self):
        script = """
        $ cd /
        $ ls
        dir a
        14848514 b.txt
        8504156 c.dat
        dir d
        $ cd a
        $ ls
        dir e
        29116 f
        2557 g
        62596 h.lst
        $ cd e
        $ ls
        584 i
        $ cd ..
        $ cd ..
        $ cd d
        $ ls
        4060174 j
        8033020 d.log
        5626152 d.ext
        7214296 k
        """
        lines = sanitize_data(script)
        parsed_lines = parse_input_data(lines)
        a_filesystem = filesystem_factory(parsed_lines)
        a_filesystem.calculate_directory_size(a_filesystem.root)
        a_filesystem.calculate_answer_one(a_filesystem.root)
        self.assertEqual(a_filesystem.answer_one, 95437)
        total_used_space = a_filesystem.root.size
        self.assertEqual(total_used_space, 48381165)
        a_filesystem.calculate_answer_two()
        self.assertEqual(a_filesystem.answer_two, 24933642)


def main():
    with open("input.dat", "r") as f_hdl:
        str_data = f_hdl.read()
        lines = sanitize_data(str_data)
        parsed_lines = parse_input_data(lines)
        a_filesystem = filesystem_factory(parsed_lines)
        a_filesystem.calculate_directory_size(a_filesystem.root)
        a_filesystem.calculate_answer_one(a_filesystem.root)
        print(a_filesystem.answer_one)
        a_filesystem.calculate_answer_two()
        print(a_filesystem.answer_two)
        

if __name__ == "__main__":
    main()


# if __name__ == '__main__':
#    unittest.main()
