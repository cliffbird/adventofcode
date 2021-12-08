from copy import deepcopy
from main import BaseProcessor
import re

class D24Processor(BaseProcessor):
    def run_all(self):
        self.base_run(path_suffix="example")
        self.base_run()

    def run1(self):
        tiles = Tiles()
        with open(self.path, "r") as f:
            for line in f:
                line = line.strip()
                tiles.flip_tile(line)
        print(f"part1: {tiles.get_num_black()}")
        self.tiles = tiles


    def run2(self):
        for day in range(1,100+1):
            num_black = self.tiles.do_day()
            print(f"Day {day}: {num_black}")


DIRS = ["e", "se", "sw", "w", "nw", "ne"]

class Tiles:
    def __init__(self):
        self.map = {} # key is a tuple of x,y; value is boolean (True for black, False for white, everything defaults to white)

    def flip_tile(self, line):
        coord = self.get_coord(line)
        if coord in self.map:
            self.map[coord] = not self.map[coord]
        else:
            self.map[coord] = True

    def get_coord(self, line):
        x = 0
        y = 0
        x_multiplier = 2
        for index in range(len(line)):
            cur_dir = line[index]
            if cur_dir == "n":
                y += 2
                x_multiplier = 1
            elif cur_dir == "s":
                y -= 2
                x_multiplier = 1
            elif cur_dir == "e":
                x += x_multiplier
                x_multiplier = 2
            elif cur_dir == "w":
                x -= x_multiplier
                x_multiplier = 2
        return x, y

    def get_neighbor_coords(self, coord):
        x = coord[0]
        y = coord[1]
        # e, w, ne, se, nw, sw
        return [(x+2, y), (x-2, y), (x+1, y+2), (x+1, y-2), (x-1, y+2), (x-1, y-2)]

    def get_black_coords(self):
        black_coords = set()
        for coord, value in self.map.items():
            if value:
                black_coords.add(coord)
        return black_coords

    def get_num_black(self):
        num_black = 0
        for coord, value in self.map.items():
            if value:
                num_black += 1
        return num_black

    def do_day(self):
        counts_map = {}

        black_coords = self.get_black_coords()
        for coord in black_coords:
            neighbors = self.get_neighbor_coords(coord)
            for neighbor in neighbors:
                if neighbor in counts_map:
                    counts_map[neighbor] += 1
                else:
                    counts_map[neighbor] = 1

        new_map = {}

        num_black = 0
        for coord, count in counts_map.items():
            if coord not in self.map or not self.map[coord]:
                if count == 2:
                    new_map[coord] = True
                    num_black += 1
            else:
                if count == 0 or count > 2:
                    new_map[coord] = False
                else:
                    new_map[coord] = True
                    num_black += 1

        self.map = new_map
        return num_black
