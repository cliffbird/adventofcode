from copy import copy
from main import BaseProcessor

class D5Processor(BaseProcessor):

    def setup(self):
        self.x_max = 0
        self.y_max = 0

        lines = None
        with open(self.path, "r") as f:
            lines = f.readlines()
        self.lines = lines
        for line in lines:
            line = line.strip()
            start, end = line.split(" -> ")
            start_x, start_y = start.split(",")
            start_x = int(start_x)
            start_y = int(start_y)
            end_x, end_y = end.split(",")
            end_x = int(end_x)
            end_y = int(end_y)

            if start_x > self.x_max:
                self.x_max = start_x
            if end_x > self.x_max:
                self.x_max = end_x
            if start_y > self.y_max:
                self.y_max = start_y
            if end_y > self.y_max:
                self.y_max = end_y

            if start_x == end_x:
                pass
            elif start_y == end_y:
                pass

        self.grid = []
        for i in range(self.y_max+1):
            row = []
            for j in range(self.x_max+1):
                row.append(0)
            self.grid.append(row)


    def run1(self):
        self.setup()

        for line in self.lines:
            line = line.strip()
            start, end = line.split(" -> ")
            start_x, start_y = start.split(",")
            start_x = int(start_x)
            start_y = int(start_y)
            end_x, end_y = end.split(",")
            end_x = int(end_x)
            end_y = int(end_y)

            if start_x > end_x:
                temp = start_x
                start_x = end_x
                end_x = temp
            if start_y > end_y:
                temp = start_y
                start_y = end_y
                end_y = temp

            if start_x == end_x:
                for y in range(start_y, end_y + 1):
                    self.grid[y][start_x] += 1
            elif start_y == end_y:
                for x in range(start_x, end_x + 1):
                    self.grid[start_y][x] += 1

        num_points = 0
        for row in self.grid:
            for value in row:
                if value > 1:
                    num_points += 1
        print(f"part1: {num_points}")

    def run2(self):
        for i in range(self.y_max + 1):
            for j in range(self.x_max + 1):
                self.grid[j][i] = 0
        for line in self.lines:
            line = line.strip()
            start, end = line.split(" -> ")
            start_x, start_y = start.split(",")
            start_x = int(start_x)
            start_y = int(start_y)
            end_x, end_y = end.split(",")
            end_x = int(end_x)
            end_y = int(end_y)


            if start_x == end_x or start_y == end_y:
                if start_x > end_x:
                    temp = start_x
                    start_x = end_x
                    end_x = temp
                if start_y > end_y:
                    temp = start_y
                    start_y = end_y
                    end_y = temp

                if start_x == end_x:
                    for y in range(start_y, end_y + 1):
                        self.grid[y][start_x] += 1
                elif start_y == end_y:
                    for x in range(start_x, end_x + 1):
                        self.grid[start_y][x] += 1
            elif abs(end_x - start_x) == abs(end_y - start_y):
                if start_x > end_x:
                    x_step = -1
                else:
                    x_step = 1

                if start_y > end_y:
                    y_step = -1
                else:
                    y_step = 1


                pre = self.grid[end_y][end_x]
                for i in range(abs(end_x - start_x) + 1):
                    y = start_y + (i * y_step)
                    x = start_x + (i * x_step)
                    self.grid[y][x] += 1
            else:
                print(f"ERROR: start_x, start_y -> end_x, end_y: {end_x - start_x}, {end_y - start_y}")

        num_points = 0
        for row in self.grid:
            for value in row:
                if value > 1:
                    num_points += 1
        print(f"part2: {num_points}")


class Board:
    NUM_DIAGONALS = 2
    def __init__(self, length):
        self.length = length
        self.rows = []
        self.sets = []
        self.remaining = set()

    def set_row(self, line):
        row = line.split()
        assert len(row) == self.length
        cur_row = []
        for value in row:
            cur_row.append(int(value))
        self.rows.append(cur_row)
        if len(self.rows) == self.length:
            self.set_sets()

    def set_sets(self):
        # create rows (with sets) and columns
        rows = []
        columns = []
        for i in range(self.length):
            rows.append(set())
            columns.append(set())
        for i, row in enumerate(self.rows):
            for j, value in enumerate(row):
                rows[i].add(value)
                columns[j].add(value)
                self.remaining.add(value)
        for i in range(self.length):
            self.sets.append(rows[i])
            self.sets.append(columns[i])

        # create diagonals
        diagonals = [set(), set()]
        for i in range(self.length):
            diagonals[0].add(self.rows[i][i])
            diagonals[1].add(self.rows[i][self.length - i - 1])
        self.sets.append(diagonals[0])
        self.sets.append(diagonals[1])

    def mark(self, value):
        try:
            self.remaining.remove(value)
        except KeyError:
            pass
        for cur_set in self.sets:
            try:
                cur_set.remove(value)
            except KeyError:
                pass

    def has_winner(self):
        for cur_set in self.sets:
            if len(cur_set) == 0:
                return True
        return False

    def get_remaining_total(self):
        total = 0
        for value in self.remaining:
            total += value
        return total
