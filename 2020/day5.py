from main import BaseProcessor


class D5Processor(BaseProcessor):
    NUM_ROWS = 128
    NUM_COLS = 8

    def run1(self):
        self.taken = set()
        self.max_seat_id = 0
        line_number = 0
        with open(self.path, "r") as f:
            for line in f:
                line = line.strip()
                row = self.get_row(line)
                seat = self.get_seat(line)
                seat_id = row * 8 + seat
                self.taken.add(seat_id)
                if seat_id > self.max_seat_id:
                    self.max_seat_id = seat_id
                line_number += 1
        print(f"max seat ID: {self.max_seat_id}")

    def get_row(self, boarding_pass):
        cur_range = (0, self.NUM_ROWS - 1)
        row_part = boarding_pass[:7]
        half = int(self.NUM_ROWS / 2)
        for index in range(len(row_part)):
            char = row_part[index]
            if char == "F":
                cur_range = (cur_range[0], cur_range[1] - half)
            elif char == "B":
                cur_range = (cur_range[0] + half, cur_range[1])
            else:
                raise Exception(f"Invalid character {char}")
            half = int(half/2)
        assert cur_range[0] == cur_range[1]
        return cur_range[0]

    def get_seat(self, boarding_pass):
        cur_range = (0, self.NUM_COLS - 1)
        seat_part = boarding_pass[7:]
        half = int(self.NUM_COLS / 2)
        for index in range(len(seat_part)):
            char = seat_part[index]
            if char == "L":
                cur_range = (cur_range[0], cur_range[1] - half)
            elif char == "R":
                cur_range = (cur_range[0] + half, cur_range[1])
            else:
                raise Exception(f"Invalid character {char}")
            half = int(half / 2)
        assert cur_range[0] == cur_range[1]
        return cur_range[0]

    def run2(self):

        min = self.max_seat_id
        for seat_id in self.taken:
            if seat_id < min:
                min = seat_id
        all_seats = list(range(min, self.max_seat_id + 1))
        for seat_id in self.taken:
            all_seats.remove(seat_id)
        print(f"my seat ID: {all_seats[0]}")