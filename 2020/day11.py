from copy import deepcopy
from main import BaseProcessor

class D11Processor(BaseProcessor):
    def run1(self):
        self.part_name = "part1"
        self.should_be_empty = self.should_be_empty_part1
        self.define_adjacent_rules = self.define_adjacent_rules_part1
        self.run()

    def run2(self):
        self.part_name = "part2"
        self.should_be_empty = self.should_be_empty_part2
        self.define_adjacent_rules = self.define_adjacent_rules_part2
        self.run()

    def run(self):
        self.seats = []
        self.seat_locations = []
        with open(self.path, "r") as f:
            for line in f:
                row = []
                line = line.strip()
                col_num = 0
                for char in line:
                    row.append(char)
                    if char == "L":
                        self.seat_locations.append((len(self.seats), col_num))
                    col_num += 1
                self.seats.append(row)
        self.num_rows = len(self.seats)
        self.num_cols = len(self.seats[0])
        self.define_adjacent_rules(self.seats)

        while True:
            new_seats = self.run_round()
            if self.do_seat_maps_match(self.seat_locations, self.seats, new_seats):
                print(f"{self.part_name}: Seats haven't changed! Num occupied {self.get_num_occupied(new_seats)}")
                break
            self.seats = new_seats

    def run_round(self):
        new_seats = deepcopy(self.seats)
        for seat_location in self.seat_locations:
            row_num = seat_location[0]
            col_num = seat_location[1]
            if self.get_seat_from_location(seat_location) == "L" and not self.is_adjacent_occupied(row_num, col_num):
                self.set_seat(new_seats, row_num, col_num, "#")
            elif self.get_seat_from_location(seat_location) == "#" and self.should_be_empty(row_num, col_num):
                self.set_seat(new_seats, row_num, col_num, "L")
        return new_seats

    def is_adjacent_occupied(self, row_num, col_num):
        adjacent_seats = self.adjacent_rules[(row_num, col_num)]
        for adjacent_seat in adjacent_seats:
            seat = self.get_seat_from_location(adjacent_seat)
            if seat and seat == "#":
                return True
        return False

    def should_be_empty_part1(self, row_num, col_num):
        return self.get_num_adjacent_occupied(row_num, col_num) >= 4

    def should_be_empty_part2(self, row_num, col_num):
        return self.get_num_adjacent_occupied(row_num, col_num) >= 5

    def get_num_adjacent_occupied(self, row_num, col_num):
        adjacent = self.get_adjacent(row_num, col_num)
        num_occupied = 0
        for seat in adjacent:
            if seat == "#":
                num_occupied += 1
        return num_occupied

    def get_adjacent(self, row_num, col_num):
        adjacent_values = []
        adjacent_seats = self.adjacent_rules[(row_num, col_num)]
        for adjacent_seat in adjacent_seats:
            seat = self.get_seat_from_location(adjacent_seat)
            adjacent_values.append(seat)
        return adjacent_values

    def define_adjacent_rules_part1(self, seats):
        self.adjacent_rules = {}
        for row_num in range(len(seats)):
            row = seats[row_num]
            for col_num in range(len(row)):
                seats_to_check = []
                for r_delta, c_delta in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                    cur_r = row_num + r_delta
                    cur_c = col_num + c_delta
                    next_seat = self.get_seat_with_validation(cur_r, cur_c)
                    if next_seat == "L":
                        seats_to_check.append((cur_r, cur_c))

                self.adjacent_rules[(row_num, col_num)] = seats_to_check

    def define_adjacent_rules_part2(self, seats):
        self.adjacent_rules = {}
        for row_num in range(len(seats)):
            row = seats[row_num]
            for col_num in range(len(row)):
                seats_to_check = []
                for r_delta, c_delta in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
                    cur_r = row_num + r_delta
                    cur_c = col_num + c_delta
                    next_seat = self.get_seat_with_validation(cur_r, cur_c)
                    while next_seat:
                        if next_seat == "L":
                            seats_to_check.append((cur_r, cur_c))
                            break

                        cur_r = cur_r + r_delta
                        cur_c = cur_c + c_delta
                        next_seat = self.get_seat_with_validation(cur_r, cur_c)

                self.adjacent_rules[(row_num, col_num)] = seats_to_check

    def get_adjacent_part2(self, row_num, col_num):
        adjacent = []
        for r in [row_num-1, row_num, row_num+1]:
            for c in [col_num-1, col_num, col_num+1]:
                if r == row_num and c == col_num:
                    continue
                seat = self.get_seat_from_location((r, c))
                if seat:
                    adjacent.append(seat)
        return adjacent

    def get_seat_with_validation(self, row_num, col_num):
        if self.is_row_num_valid(row_num) and self.is_col_num_valid(col_num):
            seat = self.seats[row_num][col_num]
        else:
            seat = None
        return seat

    def get_seat_from_location(self, seat_location):
        return self.seats[seat_location[0]][seat_location[1]]

    def is_row_num_valid(self, row_num):
        return row_num >= 0 and row_num < self.num_rows

    def is_col_num_valid(self, col_num):
        return col_num >= 0 and col_num < self.num_cols

    @classmethod
    def set_seat(cls, seats, row_num, col_num, value):
        assert seats[row_num][col_num] != "."
        seats[row_num][col_num] = value

    @classmethod
    def print_seats(cls, seats):
        for row in seats:
            print("".join(row))

    @classmethod
    def do_seat_maps_match(cls, seat_locations, seats1, seats2):
        for seat_location in seat_locations:
            row_num = seat_location[0]
            col_num = seat_location[1]
            if seats1[row_num][col_num] != seats2[row_num][col_num]:
                return False
        """
        for row_num in range(len(seats1)):
            row1 = seats1[row_num]
            row2 = seats2[row_num]
            for col_num in range(len(row1)):
                if row1[col_num] != row2[col_num]:
                    return False
        """
        return True

    @classmethod
    def get_num_occupied(cls, seats):
        num_occupied = 0
        for row_num in range(len(seats)):
            row = seats[row_num]
            for col_num in range(len(row)):
                if row[col_num] == "#":
                    num_occupied += 1
        return num_occupied
