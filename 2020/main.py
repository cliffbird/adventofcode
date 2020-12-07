import argparse
import math
import os
import re
import sys
import time


class BaseProcessor:
    INPUT_PATH_FORMAT = os.path.join("input", "day{}.txt")
    EXAMPLE_PATH_FORMAT = os.path.join("input", "day{}_example.txt")

    def __init__(self, day, example):
        self.example = example

        self.path = self.get_path_from_day(day)


    def get_path_from_day(self, day):
        if self.example:
            return self.EXAMPLE_PATH_FORMAT.format(day)
        else:
            return self.INPUT_PATH_FORMAT.format(day)


class D1Processor(BaseProcessor):
    SUM = 2020
    EQUAL_POINT = 1010

    def init(self):
        data_list = []
        with open(self.get_path_from_day(day), "r") as f:
            for line in f:
                data_list.append(int(line.strip()))

        self.data_list = data_list
        self.data_list.sort()

    def run1(self):
        self.init()
        self.do_double()

    def do_double(self):
        lower = set()
        upper = set()
        equal = []

        for value in self.data_list:
            if value < self.EQUAL_POINT:
                lower.add(value)
            elif value > self.EQUAL_POINT:
                upper.add(value)
            else:
                equal.append(value)

        if len(equal) > 1:
            print(f"Multiple {self.EQUAL_POINT} found: {self.EQUAL_POINT*self.EQUAL_POINT}")

        for value in lower:
            difference = self.SUM - value
            if difference in upper:
                answer = value * difference
                print(f"{value} * {difference} = {answer}")

    def run2(self):
        self.init()
        self.do_triple()

    def do_triple(self):
        for i1 in range(len(self.data_list)):
            v1 = self.data_list[i1]
            for i2 in range(len(self.data_list)):
                if i1 == i2:
                    continue
                v2 = self.data_list[i2]
                difference = self.SUM - v1 - v2
                if difference < 0:
                    break
                # binary search difference
                i3 = self.get_value_index(difference)
                if i3:
                    v3 = self.data_list[i3]
                    answer = v1*v2*v3
                    print(f"{v1} * {v2} * {v3}= {answer}")

    def get_value_index(self, find_value):
        index = int(len(self.data_list) / 2)
        width = index
        while True:
            cur_value = self.data_list[index]
            if cur_value == find_value:
                return index
            elif cur_value > find_value:
                # find below
                width = int(width / 2)
                new_index = index - width
                if new_index == index:
                    break
            else:
                # find above
                width = int(width / 2)
                new_index = index - width
                if new_index == index:
                    break
            index = new_index
        return None

class D2Processor(BaseProcessor):
    def run1(self):
        self.parse_valid()

    def parse_valid(self):
        valid_count = 0
        with open(self.path, "r") as f:
            for line in f:
                min_max, letter_colon, word = line.split()
                min, max = min_max.split("-")
                min = int(min)
                max = int(max)

                letter = letter_colon[:-1]
                letter_count = 0
                for index in range(len(word)):
                    char = word[index]
                    if char == letter:
                        letter_count += 1
                if letter_count >= min and letter_count <= max:
                    valid_count += 1

        print(f"part1 num valid: {valid_count}")

    def run2(self):
        self.parse_valid2()

    def parse_valid2(self):
        valid_count = 0
        with open(self.path, "r") as f:
            for line in f:
                min_max, letter_colon, word = line.split()
                min, max = min_max.split("-")
                min = int(min)
                max = int(max)

                letter = letter_colon[:-1]
                num_matches = 0
                if word[min-1] == letter:
                    num_matches += 1
                if word[max-1] == letter:
                    num_matches += 1
                if num_matches == 1:
                    valid_count += 1

        print(f"part2 num valid: {valid_count}")


class D3Processor(BaseProcessor):
    def run1(self):
        self.traverse(3, 1)

    def traverse(self, col_shift=1, row_shift=3):
        num_trees = 0
        row = 0
        col = 0
        with open(self.path, "r") as f:
            for line in f:
                if not row % row_shift:
                    char = line[col]
                    if char != '.':
                        num_trees += 1

                    col += col_shift
                    col = col % len(line.strip())

                row += 1

        print(f"right {col_shift}, down {row_shift}, num trees: {num_trees}")
        return num_trees

    def run2(self):
        v1 = self.traverse(1, 1)
        v2 = self.traverse(3, 1)
        v3 = self.traverse(5, 1)
        v4 = self.traverse(7, 1)
        v5 = self.traverse(1, 2)
        ans = v1*v2*v3*v4*v5
        print(f"{v1}*{v2}*{v3}*{v4}*{v5} = {ans}")


class D4Processor(BaseProcessor):
    KEYS = ["byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"]
    VALID_ECLS = ["amb", "blu", "brn", "gry", "grn", "hzl", "oth"]

    def run1(self):
        self.run("e:/vms/vmshare/adventofcode/input_day4invalid.txt")
        self.run("e:/vms/vmshare/adventofcode/input_day4valid.txt")
        self.run("e:/vms/vmshare/adventofcode/input_day4example.txt")
        self.run(self.path)

    def run(self, path):
        optional = ["cid"]
        num_valid = 0
        with open(path, "r") as f:
            valid_keys = list(self.KEYS)
            for line in f:
                line = line.strip()
                if not line:
                    # blank line
                    if len(valid_keys) == 0:
                        num_valid += 1
                    valid_keys = list(self.KEYS)

                parts = line.split()
                for part in parts:
                    key, value = part.split(":")
                    if key in valid_keys:
                        can_remove = False
                        if key == "byr":
                            try:
                                value = int(value)
                                if value >= 1920 and value <= 2002:
                                    can_remove = True
                            except:
                                pass
                        elif key == "iyr":
                            try:
                                value = int(value)
                                if value >= 2010 and value <= 2020:
                                    can_remove = True
                            except:
                                pass
                        elif key == "eyr":
                            try:
                                value = int(value)
                                if value >= 2020 and value <= 2030:
                                    can_remove = True
                            except:
                                pass
                        elif key == "hgt":
                            if "cm" in value:
                                m = re.match("([0-9]{3})cm\\Z", value)
                                if m:
                                    value = int(m.group(1))
                                    if value >= 150 and value <= 193:
                                        can_remove = True
                            elif "in" in value:
                                m = re.match("([0-9]{2})in\\Z", value)
                                if m:
                                    value = int(m.group(1))
                                    if value >= 59 and value <= 76:
                                        can_remove = True
                        elif key == "hcl":
                            m = re.match("#[0-9a-f]{6}\\Z", value)
                            if m:
                                can_remove = True
                        elif key == "ecl":
                            if value in self.VALID_ECLS:
                                can_remove = True
                        elif key == "pid":
                            m = re.match("\\A[0-9]{9}\\Z", value)
                            if m:
                                can_remove = True

                        if can_remove:
                            valid_keys.remove(key)
                for opt in optional:
                    if opt in valid_keys:
                        valid_keys.remove(opt)
            if len(valid_keys) == 0:
                num_valid += 1

        print(f"num valid: {num_valid}")
        return num_valid

    def run2(self):
        pass

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


class D6Processor(BaseProcessor):
    def run1(self):
        groups = []
        group = set()
        with open(self.path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    groups.append(group)
                    group = set()
                else:
                    for index in range(len(line)):
                        char = line[index]
                        group.add(char)
        groups.append(group)

        sum = 0
        for group in groups:
            sum += len(group)
        print(f"sum: {sum}")

    def run2(self):
        groups = []
        group = None
        with open(self.path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    groups.append(group)
                    group = None
                else:
                    if group is not None:
                        to_remove = set()
                        for char in group:
                            if char not in line:
                                to_remove.add(char)
                        for char in to_remove:
                            group.remove(char)
                    else:
                        group = set()
                        for index in range(len(line)):
                            char = line[index]
                            group.add(char)
        groups.append(group)

        sum = 0
        for group in groups:
            sum += len(group)
        print(f"sum: {sum}")

class D7Processor(BaseProcessor):
    MAIN_BAGS = ["mirrored silver"]

    def parse(self):
        outer_bag_colors_with_gold = set()
        contain_map = {}
        with open(self.path, "r") as f:
            for line in f:
                line = line.strip()
                parts = line.split(" contain ")
                left = parts[0]
                right = parts[1]

                l_parts = left.split()
                l_adj = l_parts[0]
                l_color = l_parts[1]

                contain_map[f"{l_adj} {l_color}"] = set()

                r_parts = right.split(",")
                for r_part in r_parts:
                    if "no other bags" in r_part:
                        continue
                    inner_parts = r_part.split()
                    r_num = inner_parts[0]
                    r_adj = inner_parts[1]
                    r_color = inner_parts[2]

                    contain_map[f"{l_adj} {l_color}"].add(f"{r_adj} {r_color}")
                    if r_adj == "shiny" and r_color == "gold":
                        outer_bag_colors_with_gold.add(f"{l_adj} {l_color}")
        while True:
            added_sub_bag = False
            for outer_bag, outer_bag_set in contain_map.items():
                if outer_bag in outer_bag_colors_with_gold:
                    continue
                for color_find in set(outer_bag_colors_with_gold):
                    if color_find in outer_bag_set:
                        outer_bag_colors_with_gold.add(outer_bag)
                        added_sub_bag = True
            if not added_sub_bag:
                break
        return len(outer_bag_colors_with_gold)

    def run1(self):
        count = self.parse()
        print(f"part1: {count}")

    def run2(self):
        outer_bag_colors_with_gold = set()
        contain_map = {}
        with open(self.path, "r") as f:
            for line in f:
                line = line.strip()
                parts = line.split(" contain ")
                left = parts[0]
                right = parts[1]

                l_parts = left.split()
                l_color = f"{l_parts[0]} {l_parts[1]}"

                contain_map[l_color] = []

                r_parts = right.split(",")
                for r_part in r_parts:
                    if "no other bags" in r_part:
                        continue
                    inner_parts = r_part.split()
                    r_num = int(inner_parts[0])
                    r_color = f"{inner_parts[1]} {inner_parts[2]}"

                    contain_map[l_color].append((r_num, r_color))

        self.contain_map = contain_map
        count = self.get_bag_count("shiny gold")
        print(f"part2: {count}")

    def get_bag_count(self, color):
        total = 0
        list_to_check = self.contain_map[color]
        for item in list_to_check:
            i_count = item[0]
            i_color = item[1]

            total += i_count + i_count * self.get_bag_count(i_color)

        return total


def main():
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter,
                                     description="Compare RBD names")
    parser.add_argument("day", type=int)
    parser.add_argument("-e", "--example", action="store_true")

    args = parser.parse_args()

    start_time = time.time()
    processor_class = globals()[f"D{args.day}Processor"]
    p = processor_class(args.day, args.example)
    p.run1()
    p.run2()
    print(f"Run time: {time.time() - start_time:0.3f}s")

if __name__ == "__main__":
    main()
