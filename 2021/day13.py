from collections import Counter
from copy import copy, deepcopy
from main import BaseProcessor


class D13Processor(BaseProcessor):

    def setup(self):
        height = 0
        length = 0
        instructions_part = 0
        with open(self.path, "r") as f:
            for i, line in enumerate(f):
                line = line.strip()
                if not line:
                    instructions_part += 1
                    continue
                if instructions_part == 0:
                    x, y = line.split(",")
                    x = int(x)
                    y = int(y)
                    if x + 1 > length:
                        length = x + 1
                    if y + 1 > height:
                        height = y + 1
                elif instructions_part == 1:
                    pass
                else:
                    print(f"ERROR: wrong part: {instructions_part}")


        self.paper = Paper(height, length)

        instructions_part = 0
        with open(self.path, "r") as f:
            for i, line in enumerate(f):
                line = line.strip()
                if not line:
                    instructions_part += 1
                    continue

                if instructions_part == 0:
                    x, y = line.split(",")
                    self.paper.add_point(int(x), int(y))
                elif instructions_part == 1:
                    axis, value = line[11:].split("=")
                    if axis == 'x':
                        self.paper.add_fold(x=int(value))
                        #self.paper.print()
                    elif axis == 'y':
                        self.paper.add_fold(y=int(value))
                        #self.paper.print()
                    else:
                        print(f"ERROR: wrong axis: {axis}")

        self.paper.print()
        print(f"part2: {0}")


    def run1(self):
        self.setup()

    def run2(self):
        pass

class Paper:
    def __init__(self, height, length):
        self.height = height
        self.length = length
        self.rows = []
        for i in range(height):
            row = []
            for j in range(length):
                row.append('.')
            self.rows.append(row)

        self.num_folds = 0

    def add_point(self, x, y):
        self.rows[y][x] = '#'

    def add_fold(self, x=None, y=None):
        if x:

            # merge right section
            width_left = x
            width_right = self.length - x
            if width_left >= width_right:
                source_start = self.length - 1
            else:
                source_start = (2 * x)
            source_end = x + 1
            merge_width = source_start - source_end + 1

            target_start = x - merge_width
            target_end = x

            new_paper = deepcopy(self.rows)

            for i in range(self.height):
                for j in range(merge_width):
                    if self.rows[i][source_start - j] == '#':
                        new_paper[i][target_start + j] = '#'

            for i in range(self.height):
                while len(new_paper[i]) != width_left:
                    del new_paper[i][-1]

            self.rows = new_paper
            self.length = width_left

        elif y:

            # merge bottom section
            height_top = y
            height_bottom = len(self.rows) - y
            if height_top >= height_bottom:
                source_start = len(self.rows) - 1
            else:
                source_start = (2 * y)
            source_end = y + 1
            merge_height = source_start - source_end + 1

            target_start = y - merge_height
            target_end = y

            new_paper = deepcopy(self.rows)

            for i in range(merge_height):
                for j in range(self.length):
                    if self.rows[source_start - i][j] == '#':
                        new_paper[target_start + i][j] = '#'

            while len(new_paper) != height_top:
                del new_paper[-1]

            self.rows = new_paper
            self.height = height_top


        if self.num_folds == 0:
            print(f"part1: {self.num_dots()}")
        self.num_folds += 1


    def print(self):
        for i, row in enumerate(self.rows):
            print(f"{i}: ", end="")
            for char in row:
                print(char, end="")
            print()

    def num_dots(self):
        total_dots = 0
        for row in self.rows:
            for char in row:
                if char == '#':
                    total_dots += 1
        return total_dots