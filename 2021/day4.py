from copy import copy
from main import BaseProcessor

class D4Processor(BaseProcessor):

    def setup(self, length):
        self.order = []
        self.boards = set()
        with open(self.path, "r") as f:
            lines = f.readlines()
            for value in lines[0].strip().split(","):
                self.order.append(int(value))
            line_count = 0
            for i, line in enumerate(lines[2:]):
                line = line.strip()
                if not line:
                    continue

                if line_count == 0:
                    board = Board(length)
                board.set_row(line)
                line_count += 1
                if line_count == length:
                    self.boards.add(board)
                    line_count = 0

    def run1(self):
        self.setup(5)
        for value in self.order:
            for board in self.boards:
                board.mark(value)
                if board.has_winner():
                    print(f"part1: {board.get_remaining_total()*value}")
                    break
            if board.has_winner():
                break
        pass

    def run2(self):
        self.setup(5)
        score = None
        for value in self.order:
            boards_to_remove = set()
            for board in self.boards:
                board.mark(value)
                if board.has_winner():
                    score = board.get_remaining_total()*value
                    print(f"part2: {score}")
                    boards_to_remove.add(board)

            for board in boards_to_remove:
                self.boards.remove(board)
        pass


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
