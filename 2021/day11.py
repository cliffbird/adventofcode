from collections import Counter
from copy import copy
from main import BaseProcessor

class D11Processor(BaseProcessor):

    def setup(self):
        grid = Grid()
        with open(self.path, "r") as f:
            for i, line in enumerate(f):
                for j, char in enumerate(line.strip()):
                    value = int(char)
                    grid.rows[i][j].level = value

        step = 0
        while True:
            step += 1
            grid.increase_all()
            print(f"step {step}: {grid.total_flashes}")
            #grid.print()
            if grid.all:
                break

    def run1(self):
        self.setup()

    def run2(self):
        pass

class Grid:
    DIM = 10
    def __init__(self):
        self.rows = []
        for i in range(self.DIM):
            row = []
            for j in range(self.DIM):
                row.append(Point(i,j, self))
            self.rows.append(row)

        for row in self.rows:
            for p in row:
                p.add_neighbors()

        self.total_flashes = 0
        self.num_flashes = [0]

        self.will_flash = set()
        self.has_flashed = set()

        self.all = False

    def increase_all(self):
        set_to_increase = set()
        for row in self.rows:
            for p in row:
                set_to_increase.add(p)
        self.increase_set(set_to_increase)

    def increase_set(self, set_to_increase):
        num_flashes = 0

        num_flashes = 0
        while set_to_increase:
            set_to_increase_copy = copy(set_to_increase)
            set_to_increase = set()

            while set_to_increase_copy:
                p = set_to_increase_copy.pop()
                p.increase()

            num_flashes += len(self.will_flash)
            while self.will_flash:
                will_flash_copy = copy(self.will_flash)
                self.will_flash = set()

                for p in will_flash_copy:
                    self.has_flashed.add(p)
                    for np in p.neighbors:
                        np.increase()
        self.total_flashes += len(self.has_flashed)

        if len(self.has_flashed) == 100:
            self.all = True

        #assert self.total_flashes == len(self.has_flashed)
        while self.has_flashed:
            p = self.has_flashed.pop()
            assert(p.level > 9)
            p.level = 0

        self.num_flashes.append(num_flashes)

    def print(self):
        for row in self.rows:
            line = ""
            for p in row:
                line += str(p.level)
            print(line)
        print()


class Point:
    def __init__(self, row, col, grid):
        self.row = row
        self.col = col
        self.grid = grid
        self.level = 0
        self.neighbors = set()
        self.has_flashed = 0

    def add_neighbors(self):
        if self.row > 0:
            prev_row = self.grid.rows[self.row - 1]
            if self.col > 0:
                self.add_neighbor(prev_row[self.col-1])
            self.add_neighbor(prev_row[self.col])
            if self.col < self.grid.DIM - 1:
                self.add_neighbor(prev_row[self.col+1])

        cur_row = self.grid.rows[self.row]
        if self.col > 0:
            self.add_neighbor(cur_row[self.col - 1])
        if self.col < self.grid.DIM - 1:
            self.add_neighbor(cur_row[self.col + 1])

        if self.row < self.grid.DIM - 1:
            next_row = self.grid.rows[self.row + 1]
            if self.col > 0:
                self.add_neighbor(next_row[self.col-1])
            self.add_neighbor(next_row[self.col])
            if self.col < self.grid.DIM - 1:
                self.add_neighbor(next_row[self.col+1])

    def add_neighbor(self, p):
        self.neighbors.add(p)

    def increase(self):
        self.level += 1
        if self.level == 10:
            if not self.has_flashed:
                self.grid.will_flash.add(self)
