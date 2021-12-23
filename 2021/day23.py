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


class D23Processor(BaseProcessor):

    def setup(self):
        grid = Grid()
        with open(self.path, "r") as f:
            for y, line in enumerate(f):
                line = line.strip()

                if y == 2:
                    order = line[3:10].split("#")
                    location = LOCATION_A0
                    for char in order:
                        ap = Amphipod(char, location)
                        grid.add_ap(ap)
                        location += 10
                elif y == 3:
                    order = line[1:8].split("#")
                    location = LOCATION_A1
                    for char in order:
                        ap = Amphipod(char, location)
                        grid.add_ap(ap)
                        location += 10
                    break

        grid.print()

        move_nodes = []
        for location in range(LOCATION_A0, LOCATION_D0 + 1, 10):
            for destination in HALLWAY_LOCATIONS:
                move_node = MoveNode(location, destination, 0, grid)
                move_node.play_next()
                if move_node.next_moves:
                    move_nodes.append(move_node)

        winners = []
        # traverse the tree
        next_nodes = copy(move_nodes)
        while next_nodes:
            move_node = next_nodes.pop()
            if move_node.is_winner:
                winners.append(move_node)
            else:
                for next_move_node in move_node.next_moves:
                    next_nodes.append(next_move_node)

        for move_node in winners:
            print(move_node.cost)


    def run1(self):
        self.setup()
        print(f"part1: {0}")

    def run2(self):
        print(f"part2: {0}")



class MoveNode:
    def __init__(self, start, destination, cost, grid):
        self.start = start
        self.destination = destination
        self.cost = cost + grid.grid[start].get_move_cost(destination)
        self.grid = deepcopy(grid)
        self.grid.move_ap(start, destination)
        self.next_moves = []
        self.is_end = False
        self.is_winner = True
        for location in ROOM_LOCATIONS:
            ap = self.grid.grid[location]
            if ap != " " and not self.grid.is_at_final(ap):
                self.is_winner = False
                break

    def __repr__(self):
        return f"{self.source}->{self.destination}"

    def play_next(self):
        for start, destination_dict in MOVE_AMOUNTS.items():
            if self.grid.grid[start] == " ":
                continue
            ap = self.grid.grid[start]
            if self.grid.is_at_final(ap):
                continue
            possible_destinations = []
            final_destinations = get_destinations(ap.type)
            if start <= LOCATION_H10:
                # can only move to final destination

                if self.grid.grid[final_destinations[0]] == " ":
                    if self.grid.is_clear(start, final_destinations[0]):
                        possible_destinations.append(final_destinations[0])
                elif self.grid.grid[final_destinations[0]].type == ap.type and \
                     self.grid.grid[final_destinations[1]] == " " and self.grid.is_clear(start, final_destinations[1]):
                    possible_destinations.append(final_destinations[1])
            else:
                for destination in MOVE_AMOUNTS[start]:
                    # can only move to the hallway or final destination
                    if (destination <= LOCATION_H10 or destination in final_destinations) and self.grid.is_clear(start, destination):
                        possible_destinations.append(destination)
            for destination in possible_destinations:
                new_node = MoveNode(start, destination, self.cost, self.grid)
                if not new_node.is_winner:
                    new_node.play_next()
                    if new_node.next_moves:
                        self.next_moves.append(new_node)



class Grid:
    def __init__(self):
        grid = {}
        # set the inbetween points
        for location in [LOCATION_H02, LOCATION_H04, LOCATION_H06, LOCATION_H08]:
            grid[location] = " "
        for location in MOVE_AMOUNTS:
            grid[location] = " "
        self.grid = grid

    def add_ap(self, ap):
        self.grid[ap.location] = ap

    def move_ap(self, start, end):
        assert self.is_clear(start, end)
        ap = self.grid[start]
        self.grid[end] = self.grid[start]
        self.grid[start] = " "
        ap.location = end

    def is_clear(self, start, end):
        is_clear = True
        locations = list(LOCATIONS_BETWEEN[start][end])
        locations.append(end)
        for location in locations:
            if self.grid[location] != " ":
                is_clear = False
                break
        return is_clear

    def print(self):
        # row 0
        for i in range(0, 13):
            print("#", end="")
        print("\n#", end="")

        # row 1
        for i in range(0, 11):
            print(str(self.grid[i]), end="")
        print("#\n###", end="")

        # row 2
        for i in range(20, 60, 10):
            print(f"{self.grid[i]}#", end="")
        print("##\n  #", end="")

        # row 3
        for i in range(21, 61, 10):
            print(f"{self.grid[i]}#", end="")
        print("\n  #########")

    def is_at_final(self, ap):
        final_destinations = ap.get_final_destinations()
        if ap.location == final_destinations[0] or \
           (ap.location == final_destinations[1] and self.grid[final_destinations[0]] != ' ' and self.grid[final_destinations[0]].type == ap.type):
            return True
        return False

def get_destinations(type):
    if type == "A":
        return [LOCATION_A1, LOCATION_A0]
    elif type == "B":
        return [LOCATION_B1, LOCATION_B0]
    elif type == "C":
        return [LOCATION_C1, LOCATION_C0]
    elif type == "D":
        return [LOCATION_D1, LOCATION_D0]

def get_move_cost(type):
    if type == "A":
        return 1
    elif type == "B":
        return 10
    elif type == "C":
        return 100
    elif type == "D":
        return 1000


class Amphipod:
    def __init__(self, type, location):
        self.type = type
        self.location = location

    def move(self, dest):
        pass

    def get_move_cost(self, destination):
        return MOVE_AMOUNTS[self.location][destination] * get_move_cost(self.type)

    def get_final_destinations(self):
        return get_destinations(self.type)

    def __str__(self):
        return self.type

    def __repr__(self):
        return f"{self.type}({self.location})"


LOCATION_H00 = 0
LOCATION_H01 = 1
LOCATION_H02 = 2
LOCATION_H03 = 3
LOCATION_H04 = 4
LOCATION_H05 = 5
LOCATION_H06 = 6
LOCATION_H07 = 7
LOCATION_H08 = 8
LOCATION_H09 = 9
LOCATION_H10 = 10
LOCATION_A0 = 20
LOCATION_A1 = 21
LOCATION_B0 = 30
LOCATION_B1 = 31
LOCATION_C0 = 40
LOCATION_C1 = 41
LOCATION_D0 = 50
LOCATION_D1 = 51

HALLWAY_LOCATIONS = [0, 1, 3, 5, 7, 9, 10]
ROOM_LOCATIONS = [LOCATION_A0, LOCATION_A1, LOCATION_B0, LOCATION_B1, LOCATION_C0, LOCATION_C1, LOCATION_D0, LOCATION_D1]


LOCATIONS_BETWEEN = {
    LOCATION_H00: {
        LOCATION_A0: [LOCATION_H01],
        LOCATION_A1: [LOCATION_H01, LOCATION_A0],
        LOCATION_B0: [LOCATION_H01, LOCATION_H03],
        LOCATION_B1: [LOCATION_H01, LOCATION_H03, LOCATION_B0],
        LOCATION_C0: [LOCATION_H01, LOCATION_H03, LOCATION_H05],
        LOCATION_C1: [LOCATION_H01, LOCATION_H03, LOCATION_H05, LOCATION_C0],
        LOCATION_D0: [LOCATION_H01, LOCATION_H03, LOCATION_H05, LOCATION_H07],
        LOCATION_D1: [LOCATION_H01, LOCATION_H03, LOCATION_H05, LOCATION_H07, LOCATION_D0]
    },
    LOCATION_H01: {
        LOCATION_A0: [],
        LOCATION_A1: [LOCATION_A0],
        LOCATION_B0: [LOCATION_H03],
        LOCATION_B1: [LOCATION_H03, LOCATION_B0],
        LOCATION_C0: [LOCATION_H03, LOCATION_H05],
        LOCATION_C1: [LOCATION_H03, LOCATION_H05, LOCATION_C0],
        LOCATION_D0: [LOCATION_H03, LOCATION_H05, LOCATION_H07],
        LOCATION_D1: [LOCATION_H03, LOCATION_H05, LOCATION_H07, LOCATION_D0]
    },
    LOCATION_H03: {
        LOCATION_A0: [],
        LOCATION_A1: [LOCATION_A0],
        LOCATION_B0: [],
        LOCATION_B1: [LOCATION_B0],
        LOCATION_C0: [LOCATION_H05],
        LOCATION_C1: [LOCATION_H05, LOCATION_C0],
        LOCATION_D0: [LOCATION_H05, LOCATION_H07],
        LOCATION_D1: [LOCATION_H05, LOCATION_H07, LOCATION_D0]
    },
    LOCATION_H05: {
        LOCATION_A0: [LOCATION_H03],
        LOCATION_A1: [LOCATION_H03, LOCATION_A0],
        LOCATION_B0: [],
        LOCATION_B1: [LOCATION_B0],
        LOCATION_C0: [],
        LOCATION_C1: [LOCATION_C0],
        LOCATION_D0: [LOCATION_H07],
        LOCATION_D1: [LOCATION_H07, LOCATION_D0]
    },
    LOCATION_H07: {
        LOCATION_A0: [LOCATION_H03, LOCATION_H05],
        LOCATION_A1: [LOCATION_H03, LOCATION_H05, LOCATION_A0],
        LOCATION_B0: [LOCATION_H03],
        LOCATION_B1: [LOCATION_H03, LOCATION_B0],
        LOCATION_C0: [],
        LOCATION_C1: [LOCATION_C0],
        LOCATION_D0: [],
        LOCATION_D1: [LOCATION_D0]
    },
    LOCATION_H09: {
        LOCATION_A0: [LOCATION_H03, LOCATION_H05, LOCATION_H07],
        LOCATION_A1: [LOCATION_H03, LOCATION_H05, LOCATION_H07, LOCATION_A0],
        LOCATION_B0: [LOCATION_H05, LOCATION_H07],
        LOCATION_B1: [LOCATION_H05, LOCATION_H07, LOCATION_B0],
        LOCATION_C0: [LOCATION_H07],
        LOCATION_C1: [LOCATION_H07, LOCATION_C0],
        LOCATION_D0: [],
        LOCATION_D1: [LOCATION_D0]
    },
    LOCATION_H10: {
        LOCATION_A0: [LOCATION_H03, LOCATION_H05, LOCATION_H07, LOCATION_H09],
        LOCATION_A1: [LOCATION_H03, LOCATION_H05, LOCATION_H07, LOCATION_H09, LOCATION_A0],
        LOCATION_B0: [LOCATION_H05, LOCATION_H07, LOCATION_H09],
        LOCATION_B1: [LOCATION_H05, LOCATION_H07, LOCATION_H09, LOCATION_B0],
        LOCATION_C0: [LOCATION_H07, LOCATION_H09],
        LOCATION_C1: [LOCATION_H07, LOCATION_H09, LOCATION_C0],
        LOCATION_D0: [LOCATION_H09],
        LOCATION_D1: [LOCATION_H09, LOCATION_D0]
    },
    LOCATION_A0: {
        LOCATION_H00: [LOCATION_H01],
        LOCATION_H01: [],
        LOCATION_H03: [],
        LOCATION_H05: [LOCATION_H03],
        LOCATION_H07: [LOCATION_H03, LOCATION_H05],
        LOCATION_H09: [LOCATION_H03, LOCATION_H05, LOCATION_H07],
        LOCATION_H10: [LOCATION_H03, LOCATION_H05, LOCATION_H07, LOCATION_H09],
        LOCATION_B0: [LOCATION_H03],
        LOCATION_B1: [LOCATION_H03, LOCATION_B0],
        LOCATION_C0: [LOCATION_H03, LOCATION_H05],
        LOCATION_C1: [LOCATION_H03, LOCATION_H05, LOCATION_C0],
        LOCATION_D0: [LOCATION_H03, LOCATION_H05, LOCATION_H07],
        LOCATION_D1: [LOCATION_H03, LOCATION_H05, LOCATION_H07, LOCATION_D0]
    },
    LOCATION_A1: {
        LOCATION_H00: [LOCATION_A0, LOCATION_H01],
        LOCATION_H01: [LOCATION_A0],
        LOCATION_H03: [LOCATION_A0],
        LOCATION_H05: [LOCATION_A0, LOCATION_H03],
        LOCATION_H07: [LOCATION_A0, LOCATION_H03, LOCATION_H05],
        LOCATION_H09: [LOCATION_A0, LOCATION_H03, LOCATION_H05, LOCATION_H07],
        LOCATION_H10: [LOCATION_A0, LOCATION_H03, LOCATION_H05, LOCATION_H07, LOCATION_H09],
        LOCATION_B0: [LOCATION_A0, LOCATION_H03],
        LOCATION_B1: [LOCATION_A0, LOCATION_H03, LOCATION_B0],
        LOCATION_C0: [LOCATION_A0, LOCATION_H03, LOCATION_H05],
        LOCATION_C1: [LOCATION_A0, LOCATION_H03, LOCATION_H05, LOCATION_C0],
        LOCATION_D0: [LOCATION_A0, LOCATION_H03, LOCATION_H05, LOCATION_H07],
        LOCATION_D1: [LOCATION_A0, LOCATION_H03, LOCATION_H05, LOCATION_H07, LOCATION_D0]
    },
    LOCATION_B0: {
        LOCATION_H00: [LOCATION_H03, LOCATION_H01],
        LOCATION_H01: [LOCATION_H03],
        LOCATION_H03: [],
        LOCATION_H05: [],
        LOCATION_H07: [LOCATION_H05],
        LOCATION_H09: [LOCATION_H05, LOCATION_H07],
        LOCATION_H10: [LOCATION_H05, LOCATION_H07, LOCATION_H09],
        LOCATION_A0: [LOCATION_H03],
        LOCATION_A1: [LOCATION_H03, LOCATION_A0],
        LOCATION_C0: [LOCATION_H05],
        LOCATION_C1: [LOCATION_H05, LOCATION_C0],
        LOCATION_D0: [LOCATION_H05, LOCATION_H07],
        LOCATION_D1: [LOCATION_H05, LOCATION_H07, LOCATION_D0]
    },
    LOCATION_B1: {
        LOCATION_H00: [LOCATION_B0, LOCATION_H03, LOCATION_H01],
        LOCATION_H01: [LOCATION_B0, LOCATION_H03],
        LOCATION_H03: [LOCATION_B0],
        LOCATION_H05: [LOCATION_B0],
        LOCATION_H07: [LOCATION_B0, LOCATION_H05],
        LOCATION_H09: [LOCATION_B0, LOCATION_H05, LOCATION_H07],
        LOCATION_H10: [LOCATION_B0, LOCATION_H05, LOCATION_H07, LOCATION_H09],
        LOCATION_A0: [LOCATION_B0, LOCATION_H03],
        LOCATION_A1: [LOCATION_B0, LOCATION_H03, LOCATION_A0],
        LOCATION_C0: [LOCATION_B0, LOCATION_H05],
        LOCATION_C1: [LOCATION_B0, LOCATION_H05, LOCATION_C0],
        LOCATION_D0: [LOCATION_B0, LOCATION_H05, LOCATION_H07],
        LOCATION_D1: [LOCATION_B0, LOCATION_H05, LOCATION_H07, LOCATION_D0]
    },
    LOCATION_C0: {
        LOCATION_H00: [LOCATION_H01, LOCATION_H03, LOCATION_H05],
        LOCATION_H01: [LOCATION_H03, LOCATION_H05],
        LOCATION_H03: [LOCATION_H05],
        LOCATION_H05: [],
        LOCATION_H07: [],
        LOCATION_H09: [LOCATION_H07],
        LOCATION_H10: [LOCATION_H07, LOCATION_H09],
        LOCATION_A0: [LOCATION_H03, LOCATION_H05],
        LOCATION_A1: [LOCATION_H03, LOCATION_H05, LOCATION_A0],
        LOCATION_B0: [LOCATION_H03],
        LOCATION_B1: [LOCATION_H03, LOCATION_B0],
        LOCATION_D0: [LOCATION_H07],
        LOCATION_D1: [LOCATION_H07, LOCATION_D0]
    },
    LOCATION_C1: {
        LOCATION_H00: [LOCATION_C0, LOCATION_H01, LOCATION_H03, LOCATION_H05],
        LOCATION_H01: [LOCATION_C0, LOCATION_H03, LOCATION_H05],
        LOCATION_H03: [LOCATION_C0, LOCATION_H05],
        LOCATION_H05: [LOCATION_C0],
        LOCATION_H07: [LOCATION_C0],
        LOCATION_H09: [LOCATION_C0, LOCATION_H07],
        LOCATION_H10: [LOCATION_C0, LOCATION_H07, LOCATION_H09],
        LOCATION_A0: [LOCATION_C0, LOCATION_H03, LOCATION_H05],
        LOCATION_A1: [LOCATION_C0, LOCATION_H03, LOCATION_H05, LOCATION_A0],
        LOCATION_B0: [LOCATION_C0, LOCATION_H03],
        LOCATION_B1: [LOCATION_C0, LOCATION_H03, LOCATION_B0],
        LOCATION_D0: [LOCATION_C0, LOCATION_H07],
        LOCATION_D1: [LOCATION_C0, LOCATION_H07, LOCATION_D0]
    },
    LOCATION_D0: {
        LOCATION_H00: [LOCATION_H01, LOCATION_H03, LOCATION_H05, LOCATION_H07],
        LOCATION_H01: [LOCATION_H03, LOCATION_H05, LOCATION_H07],
        LOCATION_H03: [LOCATION_H05, LOCATION_H07],
        LOCATION_H05: [LOCATION_H07],
        LOCATION_H07: [],
        LOCATION_H09: [],
        LOCATION_H10: [LOCATION_H09],
        LOCATION_A0: [LOCATION_H03, LOCATION_H05, LOCATION_H07],
        LOCATION_A1: [LOCATION_H03, LOCATION_H05, LOCATION_H07, LOCATION_A0],
        LOCATION_B0: [LOCATION_H05, LOCATION_H07],
        LOCATION_B1: [LOCATION_H05, LOCATION_H07, LOCATION_B0],
        LOCATION_C0: [LOCATION_H07],
        LOCATION_C1: [LOCATION_H07, LOCATION_C0]
    },
    LOCATION_D1: {
        LOCATION_H00: [LOCATION_D0, LOCATION_H01, LOCATION_H03, LOCATION_H05, LOCATION_H07],
        LOCATION_H01: [LOCATION_D0, LOCATION_H03, LOCATION_H05, LOCATION_H07],
        LOCATION_H03: [LOCATION_D0, LOCATION_H05, LOCATION_H07],
        LOCATION_H05: [LOCATION_D0, LOCATION_H07],
        LOCATION_H07: [LOCATION_D0],
        LOCATION_H09: [LOCATION_D0],
        LOCATION_H10: [LOCATION_D0, LOCATION_H09],
        LOCATION_A0: [LOCATION_D0, LOCATION_H03, LOCATION_H05, LOCATION_H07],
        LOCATION_A1: [LOCATION_D0, LOCATION_H03, LOCATION_H05, LOCATION_H07, LOCATION_A0],
        LOCATION_B0: [LOCATION_D0, LOCATION_H05, LOCATION_H07],
        LOCATION_B1: [LOCATION_D0, LOCATION_H05, LOCATION_H07, LOCATION_B0],
        LOCATION_C0: [LOCATION_D0, LOCATION_H07],
        LOCATION_C1: [LOCATION_D0, LOCATION_H07, LOCATION_C0]
    }
}

MOVE_AMOUNTS = {
    LOCATION_H00: {
        LOCATION_A0: 3,
        LOCATION_A1: 4,
        LOCATION_B0: 5,
        LOCATION_B1: 6,
        LOCATION_C0: 7,
        LOCATION_C1: 8,
        LOCATION_D0: 9,
        LOCATION_D1: 10
    },
    LOCATION_H01: {
        LOCATION_A0: 2,
        LOCATION_A1: 3,
        LOCATION_B0: 4,
        LOCATION_B1: 5,
        LOCATION_C0: 6,
        LOCATION_C1: 7,
        LOCATION_D0: 8,
        LOCATION_D1: 9
    },
    LOCATION_H03: {
        LOCATION_A0: 2,
        LOCATION_A1: 3,
        LOCATION_B0: 2,
        LOCATION_B1: 3,
        LOCATION_C0: 4,
        LOCATION_C1: 5,
        LOCATION_D0: 6,
        LOCATION_D1: 7
    },
    LOCATION_H05: {
        LOCATION_A0: 4,
        LOCATION_A1: 5,
        LOCATION_B0: 2,
        LOCATION_B1: 3,
        LOCATION_C0: 2,
        LOCATION_C1: 3,
        LOCATION_D0: 4,
        LOCATION_D1: 5
    },
    LOCATION_H07: {
        LOCATION_A0: 6,
        LOCATION_A1: 7,
        LOCATION_B0: 4,
        LOCATION_B1: 5,
        LOCATION_C0: 2,
        LOCATION_C1: 3,
        LOCATION_D0: 2,
        LOCATION_D1: 3
    },
    LOCATION_H09: {
        LOCATION_A0: 8,
        LOCATION_A1: 9,
        LOCATION_B0: 6,
        LOCATION_B1: 7,
        LOCATION_C0: 4,
        LOCATION_C1: 5,
        LOCATION_D0: 2,
        LOCATION_D1: 3
    },
    LOCATION_H10: {
        LOCATION_A0: 9,
        LOCATION_A1: 10,
        LOCATION_B0: 7,
        LOCATION_B1: 8,
        LOCATION_C0: 5,
        LOCATION_C1: 6,
        LOCATION_D0: 3,
        LOCATION_D1: 4
    },
    LOCATION_A0: {
        LOCATION_H00: 3,
        LOCATION_H01: 2,
        LOCATION_H03: 2,
        LOCATION_H05: 4,
        LOCATION_H07: 6,
        LOCATION_H09: 8,
        LOCATION_H10: 9,
        LOCATION_B0: 4,
        LOCATION_B1: 5,
        LOCATION_C0: 6,
        LOCATION_C1: 7,
        LOCATION_D0: 8,
        LOCATION_D1: 9
    },
    LOCATION_A1: {
        LOCATION_H00: 4,
        LOCATION_H01: 3,
        LOCATION_H03: 3,
        LOCATION_H05: 5,
        LOCATION_H07: 7,
        LOCATION_H09: 9,
        LOCATION_H10: 10,
        LOCATION_B0: 5,
        LOCATION_B1: 6,
        LOCATION_C0: 7,
        LOCATION_C1: 8,
        LOCATION_D0: 9,
        LOCATION_D1: 10
    },
    LOCATION_B0: {
        LOCATION_H00: 5,
        LOCATION_H01: 4,
        LOCATION_H03: 2,
        LOCATION_H05: 2,
        LOCATION_H07: 4,
        LOCATION_H09: 6,
        LOCATION_H10: 7,
        LOCATION_A0: 4,
        LOCATION_A1: 5,
        LOCATION_C0: 4,
        LOCATION_C1: 5,
        LOCATION_D0: 6,
        LOCATION_D1: 7
    },
    LOCATION_B1: {
        LOCATION_H00: 6,
        LOCATION_H01: 5,
        LOCATION_H03: 3,
        LOCATION_H05: 3,
        LOCATION_H07: 5,
        LOCATION_H09: 7,
        LOCATION_H10: 8,
        LOCATION_A0: 5,
        LOCATION_A1: 6,
        LOCATION_C0: 5,
        LOCATION_C1: 6,
        LOCATION_D0: 7,
        LOCATION_D1: 8
    },
    LOCATION_C0: {
        LOCATION_H00: 7,
        LOCATION_H01: 6,
        LOCATION_H03: 4,
        LOCATION_H05: 2,
        LOCATION_H07: 2,
        LOCATION_H09: 4,
        LOCATION_H10: 5,
        LOCATION_A0: 6,
        LOCATION_A1: 7,
        LOCATION_B0: 4,
        LOCATION_B1: 5,
        LOCATION_D0: 4,
        LOCATION_D1: 5
    },
    LOCATION_C1: {
        LOCATION_H00: 8,
        LOCATION_H01: 7,
        LOCATION_H03: 5,
        LOCATION_H05: 3,
        LOCATION_H07: 3,
        LOCATION_H09: 5,
        LOCATION_H10: 6,
        LOCATION_A0: 7,
        LOCATION_A1: 8,
        LOCATION_B0: 5,
        LOCATION_B1: 6,
        LOCATION_D0: 5,
        LOCATION_D1: 6
    },
    LOCATION_D0: {
        LOCATION_H00: 9,
        LOCATION_H01: 8,
        LOCATION_H03: 6,
        LOCATION_H05: 4,
        LOCATION_H07: 2,
        LOCATION_H09: 2,
        LOCATION_H10: 3,
        LOCATION_A0: 8,
        LOCATION_A1: 9,
        LOCATION_B0: 6,
        LOCATION_B1: 7,
        LOCATION_C0: 4,
        LOCATION_C1: 5
    },
    LOCATION_D1: {
        LOCATION_H00: 10,
        LOCATION_H01: 9,
        LOCATION_H03: 7,
        LOCATION_H05: 5,
        LOCATION_H07: 3,
        LOCATION_H09: 3,
        LOCATION_H10: 4,
        LOCATION_A0: 9,
        LOCATION_A1: 10,
        LOCATION_B0: 7,
        LOCATION_B1: 8,
        LOCATION_C0: 5,
        LOCATION_C1: 6
    }
}
