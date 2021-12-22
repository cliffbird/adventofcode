from collections import Counter
from copy import copy, deepcopy
import hashlib
from main import BaseProcessor
from math import ceil, floor, sqrt
from queue import SimpleQueue
import sys
from threading import Thread, Lock

STATE_GET_ALGORITHM = 0
STATE_GET_IMAGE = 1


class D20Processor(BaseProcessor):

    def setup(self):
        state = STATE_GET_ALGORITHM
        algorithm = Algorithm()
        image = None
        with open(self.path, "r") as f:
            for y, line in enumerate(f):
                line = line.strip()

                if not line:
                    state += 1
                    image = Image(algorithm)
                    continue

                if state == STATE_GET_ALGORITHM:
                    algorithm.add_line(line)
                elif state == STATE_GET_IMAGE:
                    image.add_line(line)

        image.finalize()
        image.print()
        print()

        for i in range(50):

            image.process_image(inplace=True)
            if i == 1:
                image.print()
                print()
            elif i == 49:
                print(f"part2: {image.get_num_lit_pixels()}")

    def run1(self):
        self.setup()

    def run2(self):
        pass


class Algorithm:
    def __init__(self):
        self.string = ""

    def add_line(self, line):
        self.string += line

    def get_output_pixel(self, value):
        return self.string[value]


class Image:
    def __init__(self, algorithm):
        self.algorithm = algorithm
        self.lines = []
        self.padding = 2

    def add_line(self, line):
        self.lines.append(line)

    def finalize(self):
        self.pad_image(True)

    def pad_image(self, override=False):
        self.height = len(self.lines)
        self.width = len(self.lines[0])
        if not override:
            padding_character = self.lines[0][0]
        else:
            padding_character = '.'
        padding_line = ""
        for i in range(self.width + (2*self.padding)):
            padding_line += padding_character
        new_lines = []
        for i in range(self.padding):
            new_lines.append(padding_line)

        front_rear_padding = ""
        for i in range(self.padding):
            front_rear_padding += padding_character
        for line in self.lines:
            new_lines.append(front_rear_padding + line + front_rear_padding)

        for i in range(self.padding):
            new_lines.append(padding_line)
        self.lines = new_lines

        self.real_height = len(self.lines)
        self.real_width = len(self.lines[0])
        for i, line in enumerate(self.lines):
            assert len(line) == self.real_width
        assert self.height == len(self.lines) - (2*self.padding)
        assert self.width == len(self.lines[0]) - (2 * self.padding)

    def process_image(self, inplace=False):
        output_lines = []

        for virt_y in range(-self.padding, self.height+self.padding):
            output_line = ""
            for virt_x in range(-self.padding, self.width+self.padding):
                output_line += self.process_pixel(virt_x, virt_y)
            output_lines.append(output_line)

        if inplace:
            self.lines = output_lines
            self.pad_image()
        return output_lines

    def process_pixel(self, virt_x, virt_y):
        value = 0
        for _virt_y in range(virt_y-1, virt_y+2):
            for _virt_x in range(virt_x-1, virt_x+2):
                value *= 2
                if self.get_pixel(_virt_x, _virt_y) == '#':
                    value += 1

        return self.algorithm.get_output_pixel(value)

    def get_pixel(self, virt_x, virt_y):
        if virt_x >= -self.padding:
            real_x = virt_x + self.padding
        else:
            real_x = 0
        if real_x >= self.real_width:
            real_x = self.real_width - 1
        width = len(self.lines[0])
        assert self.real_width == width

        if virt_y >= -self.padding:
            real_y = virt_y + self.padding
        else:
            real_y = 0
        if real_y >= self.real_height:
            real_y = self.real_height - 1
        height = len(self.lines)
        assert self.real_height == height

        line = self.lines[real_y]
        line_len = len(line)
        pixel = line[real_x]
        return pixel

    def print(self):
        for line in self.lines:
            print(line)
        print(f"{self.get_num_lit_pixels()}")

    def get_num_lit_pixels(self):
        count = 0
        for line in self.lines:
            for char in line:
                if char == '#':
                    count += 1
        return count
