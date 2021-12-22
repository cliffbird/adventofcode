from collections import Counter
from copy import copy, deepcopy
import hashlib
from main import BaseProcessor
from math import ceil, floor, sqrt
import portion
from queue import SimpleQueue
import sys
from threading import Thread, Lock
import time


class D22Processor(BaseProcessor):

    def setup(self):
        pass


    def run1(self):
        grid = Grid(-50, 50)
        cuboids = []
        with open(self.path, "r") as f:
            for y, line in enumerate(f):
                line = line.strip()
                action_str, ranges = line.split(" ")
                parts = ranges.split(",")

                range_dict = {}
                for part in parts:
                    key, range = part.split("=")
                    start, end = range.split("..")
                    range_dict[key] = portion.closed(int(start), int(end))
                if action_str == "on":
                    action = True
                else:
                    action = False
                cuboids.append(Cuboid(range_dict["x"], range_dict["y"], range_dict["z"], action, grid))

        if 1:
            count = 0
            working = cuboids
            while len(working) > 1:
                source_c = working.pop()

                reduced = []
                while working:
                    target_c = working.pop()
                    new_cuboids = reduce(target_c, source_c)
                    reduced.extend(new_cuboids)
                reduced.reverse()
                working = reduced

                if source_c.action:
                    count += source_c.get_num_on()

            if working:
                assert len(working) == 1
                c = working.pop()
                if c.action:
                    count += c.get_num_on()
            print(f"part1: {count}")

        else:
            reduced_cuboids = []
            working = cuboids
            while len(working) > 1:
                source_c = working.pop()
                target_c = working.pop()
                new_cuboids = reduce(target_c, source_c)
                working.extend(new_cuboids)
                reduced_cuboids.append(source_c)

            reduced_cuboids.extend(working)
            reduced_cuboids.reverse()

            for c in reduced_cuboids:
                c.do_action()

            print(f"part1: {grid.get_num_on()}")

    def run2(self):
        grid = Grid()
        cuboids = []
        with open(self.path, "r") as f:
            for y, line in enumerate(f):
                line = line.strip()
                action_str, ranges = line.split(" ")
                parts = ranges.split(",")

                range_dict = {}
                for part in parts:
                    key, range = part.split("=")
                    start, end = range.split("..")
                    range_dict[key] = portion.closed(int(start), int(end))
                if action_str == "on":
                    action = True
                else:
                    action = False
                cuboids.append(Cuboid(range_dict["x"], range_dict["y"], range_dict["z"], action, grid))

        count = 0
        working = cuboids
        while len(working) > 1:
            source_c = working.pop()

            reduced = []
            while working:
                target_c = working.pop()
                new_cuboids = reduce(target_c, source_c)
                reduced.extend(new_cuboids)
            reduced.reverse()
            working = reduced

            if source_c.action:
                count += source_c.get_num_on_all()

        if working:
            assert len(working) == 1
            c = working.pop()
            if c.action:
                count += c.get_num_on_all()

        print("counting...")
        print(f"part2: {count}")


class Grid:
    def __init__(self, valid_min=None, valid_max=None):
        self.valid_min = valid_min
        self.valid_max = valid_max
        self.on = {}

    def turn_on_interval(self, xyp, range_z):
        if xyp not in self.on:
            self.on[xyp] = range_z
        else:
            self.on[xyp] |= range_z

    def turn_off_interval(self, xyp, range_z):
        if xyp in self.on:
            self.on[xyp] -= range_z

    def get_num_on(self):
        num_on = 0
        for key, interval in self.on.items():
            num_on += len(list(portion.iterate(interval, 1)))
        return num_on

def reduce(target_c, source_c):
    new_cuboids = []
    count = 0

    if target_c.range_x.overlaps(source_c.range_x) and \
       target_c.range_y.overlaps(source_c.range_y) and \
       target_c.range_z.overlaps(source_c.range_z):
        overlap_x = target_c.range_x & source_c.range_x
        overlap_y = target_c.range_y & source_c.range_y
        overlap_z = target_c.range_z & source_c.range_z

        diff_x = target_c.range_x - source_c.range_x
        diff_y = target_c.range_y - source_c.range_y
        diff_z = target_c.range_z - source_c.range_z

        # do overlapping section
        for p_x in overlap_x:
            for p_y in overlap_y:
                for p_z in diff_z:
                    c = Cuboid(p_x, p_y, p_z, target_c.action, target_c.grid)
                    new_cuboids.append(c)
            for p_y in diff_y:
                c = Cuboid(p_x, p_y, target_c.range_z, target_c.action, target_c.grid)
                new_cuboids.append(c)

        # do non overlapping sections
        for p_x in diff_x:
            c = Cuboid(p_x, target_c.range_y, target_c.range_z, target_c.action, target_c.grid)
            new_cuboids.append(c)
    else:
        new_cuboids.append(target_c)

    return new_cuboids


class Cuboid:
    def __init__(self, range_x, range_y, range_z, action, grid):
        self.range_x = range_x
        self.range_y = range_y
        self.range_z = range_z
        self.action = action
        self.grid = grid

    def __repr__(self):
        return f"{self.range_x},{self.range_y},{self.range_z}"

    def is_action_on(self):
        return self.action

    def do_action(self):
        for x in portion.iterate(self.range_x & portion.closed(self.grid.valid_min, self.grid.valid_max), 1):
            for y in portion.iterate(self.range_y & portion.closed(self.grid.valid_min, self.grid.valid_max), 1):
                ref_p = Point(x,y,0)

                if self.action:
                    self.grid.turn_on_interval(ref_p, self.range_z & portion.closed(self.grid.valid_min, self.grid.valid_max))
                else:
                    self.grid.turn_off_interval(ref_p, self.range_z & portion.closed(self.grid.valid_min, self.grid.valid_max))

    def do_action_all(self):
        for x in portion.iterate(self.range_x, 1):
            for y in portion.iterate(self.range_y, 1):
                ref_p = Point(x, y, 0)

                if self.action:
                    self.grid.turn_on_interval(ref_p, self.range_z)
                else:
                    self.grid.turn_off_interval(ref_p, self.range_z)

    def get_num_on_all(self):
        num_on = 0

        if self.action:
            temp_x = self.range_x
            temp_y = self.range_y
            temp_z = self.range_z
            len_x = 0
            len_y = 0
            len_z = 0
            if not temp_x.empty:
                len_x = (temp_x.upper - temp_x.lower - 1)
                if temp_x.left == portion.CLOSED:
                    len_x += 1
                if temp_x.right == portion.CLOSED:
                    len_x += 1
            if not temp_y.empty:
                len_y = (temp_y.upper - temp_y.lower - 1)
                if temp_y.left == portion.CLOSED:
                    len_y += 1
                if temp_y.right == portion.CLOSED:
                    len_y += 1
            if not temp_z.empty:
                len_z = (temp_z.upper - temp_z.lower - 1)
                if temp_z.left == portion.CLOSED:
                    len_z += 1
                if temp_z.right == portion.CLOSED:
                    len_z += 1
            num_on = len_x * len_y * len_z

        return num_on

    def get_num_on(self):
        num_on = 0

        if self.action:
            temp_x = self.range_x & portion.closed(self.grid.valid_min, self.grid.valid_max)
            temp_y = self.range_y & portion.closed(self.grid.valid_min, self.grid.valid_max)
            temp_z = self.range_z & portion.closed(self.grid.valid_min, self.grid.valid_max)
            len_x = 0
            len_y = 0
            len_z = 0
            if not temp_x.empty:
                len_x = (temp_x.upper - temp_x.lower - 1)
                if temp_x.left == portion.CLOSED:
                    len_x += 1
                if temp_x.right == portion.CLOSED:
                    len_x += 1
            if not temp_y.empty:
                len_y = (temp_y.upper - temp_y.lower - 1)
                if temp_y.left == portion.CLOSED:
                    len_y += 1
                if temp_y.right == portion.CLOSED:
                    len_y += 1
            if not temp_z.empty:
                len_z = (temp_z.upper - temp_z.lower - 1)
                if temp_z.left == portion.CLOSED:
                    len_z += 1
                if temp_z.right == portion.CLOSED:
                    len_z += 1
            num_on = len_x * len_y * len_z

        return num_on


class Point:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __hash__(self):
        return f"{self.x},{self.y},{self.z}".__hash__()

    def __repr__(self):
        return f"{self.x},{self.y},{self.z}"
