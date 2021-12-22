from collections import Counter
from copy import copy, deepcopy
from main import BaseProcessor
from queue import SimpleQueue
import sys
from threading import Thread, Lock


class D17Processor(BaseProcessor):

    def setup(self):
        with open(self.path, "r") as f:
            for y, line in enumerate(f):
                line = line.strip()
                assert line.startswith("target area: ")
                prefix, main = line.split(": ")
                x, y = main.strip().split(", ")
                x_min, x_max = x[2:].split("..")
                self.x_min = int(x_min)
                self.x_max = int(x_max)
                y_min, y_max = y[2:].split("..")
                self.y_min = int(y_min)
                self.y_max = int(y_max)

    def run1(self):
        self.setup()

        grid = Grid()
        grid.set_target(self.x_min, self.x_max, self.y_min, self.y_max)

        vel_x_min = 1
        vel_x_max = self.x_max

        vel_y = self.y_min

        highest_y = 0
        highest_y_vel_x = None
        highest_y_vel_y = None
        target_hit_with_y = False
        is_stop = False
        count = 0
        quit_vel_y = None
        loops_with_misses_after_hit = 0
        MAX_LOOPS_WITH_MISSES_AFTER_HIT = 100

        while not is_stop:
            target_hit_with_x = False
            for vel_x in range(vel_x_min, vel_x_max+1):
                grid.set_velocity(vel_x, vel_y)
                is_hit, cur_highest_y, overshoot_x, overshoot_y = grid.do()
                if is_hit:
                    count += 1
                    print(f"HIT {count}: vel {vel_x}, {vel_y} - {cur_highest_y}")
                    if cur_highest_y > highest_y:
                        highest_y_vel_x = vel_x
                        highest_y_vel_y = vel_y
                        highest_y = cur_highest_y

                    if not target_hit_with_x:
                        target_hit_with_x = True

                    if not target_hit_with_y:
                        target_hit_with_y = True

                if overshoot_x and overshoot_y:
                    if vel_x == 2:
                        is_stop = True
            if target_hit_with_y and not target_hit_with_x:
                loops_with_misses_after_hit += 1
                if loops_with_misses_after_hit > MAX_LOOPS_WITH_MISSES_AFTER_HIT:
                    is_stop = True

            vel_y += 1

        print(f"part1: hit target with max y {highest_y} at {highest_y_vel_x, highest_y_vel_y}")
        print(f"part2: {count}")


    def run2(self):
        pass

class Grid:
    def __init__(self):
        self.clear()

    def set_target(self, x_min, x_max, y_min, y_max):
        self.target_x_min = x_min
        self.target_x_max = x_max
        self.target_y_min = y_min
        self.target_y_max = y_max

    def set_start(self, x, y):
        self.points.append((x,y))
        self.cur_x = x
        self.cur_y = y

    def set_velocity(self, x, y):
        self.clear()
        self.vel_x = x
        self.vel_y = y
        self.vel_count = 0

    def do(self):
        is_stop = False
        is_hit = False
        highest_y = 0
        overshoot_x = False
        overshoot_y = False
        while not is_stop:
            self.cur_x += self.vel_x
            self.cur_y += self.vel_y
            self.points.append((self.cur_x, self.cur_y))

            if self.vel_x > 0:
                self.vel_x -= 1
            elif self.vel_x < 0:
                self.vel_x += 1
            else:
                self.vel_x = 0

            self.vel_y -= 1

            if self.cur_y > highest_y:
                highest_y = self.cur_y

            if self.cur_y < self.target_y_min:
                overshoot_y = True
                is_stop = True

            if self.cur_x > self.target_x_max:
                overshoot_x = True
                is_stop = True

            if self.cur_x >= self.target_x_min and self.cur_x <= self.target_x_max and \
               self.cur_y >= self.target_y_min and self.cur_y <= self.target_y_max:
                is_hit = True
                is_stop = True
                #print(f"HIT: {self.cur_x}, {self.cur_y}")

        return is_hit, highest_y, overshoot_x, overshoot_y

    def clear(self):
        self.points = []
        self.set_start(0, 0)

    def print(self):
        pass
