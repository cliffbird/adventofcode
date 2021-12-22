from collections import Counter
from copy import copy, deepcopy
import hashlib
from main import BaseProcessor
from math import ceil, floor, sqrt
from queue import SimpleQueue
import sys
from threading import Thread, Lock
import time


class D21Processor(BaseProcessor):

    def setup(self):
        pass

    def run1(self):
        game = Game(DeterministicDice())
        with open(self.path, "r") as f:
            for y, line in enumerate(f):
                line = line.strip()
                player_name, position = line.split(" starting position: ")
                position = int(position)
                player_id = int(player_name.split()[1])
                game.add_player(player_id, position)

        while True:
            last_player = game.do_turn()
            if last_player.score >= 1000:
                other_player_virtual_id = (last_player.virtual_id + 1) % NUM_PLAYERS
                other_player = game.players[other_player_virtual_id]
                print(f"part1 : {other_player.score * game.dice.num_rolls}")
                break


    def run2(self):
        players = []
        with open(self.path, "r") as f:
            for y, line in enumerate(f):
                line = line.strip()
                player_name, position = line.split(" starting position: ")
                position = int(position)
                player_id = int(player_name.split()[1])
                players.append(Player(player_id-1, position))

        win_count_dict = {0: 0, 1: 0}

        start_time = time.time()

        prev_nodes = []
        cur_player_id = 0
        next_player_id = 1
        weight = 0
        for turn_value in TURN_VALUES:
            weight = TURN_VALUE_WEIGHT[turn_value]
            p1 = copy(players[0])
            p1.do_full_turn(turn_value)
            tn = TurnNode(weight, p1, copy(players[1]))
            prev_nodes.append(tn)
        cur_player_id = next_player_id

        more_turns = True
        while prev_nodes:
            cur_player_id = next_player_id
            new_prev_nodes = []

            for prev_node in prev_nodes:
                for turn_value in TURN_VALUES:
                    if cur_player_id == 0:
                        p1 = copy(prev_node.p1)
                        p2 = prev_node.p2
                        cur_player = p1
                        next_player_id = 1
                    else:
                        p1 = prev_node.p1
                        p2 = copy(prev_node.p2)
                        cur_player = p2
                        next_player_id = 0
                    cur_player.do_full_turn(turn_value)

                    weight = prev_node.weight * TURN_VALUE_WEIGHT[turn_value]
                    if cur_player.score >= 21:
                        win_count_dict[cur_player_id] += weight
                    else:
                        tn = TurnNode(weight, p1, p2)
                        new_prev_nodes.append(tn)
            prev_nodes = new_prev_nodes

        for i in range(NUM_PLAYERS):
            print(f"part2: player {i + 1} with {win_count_dict[i]}")

        print(f"Duration: {int(time.time() - start_time)} seconds")


NUM_POSITIONS = 10
NUM_PLAYERS = 2

class Game:
    def __init__(self, dice):
        self.players = {}
        self.dice = dice
        self.cur_virtual_player_id = 0

    def add_player(self, id, position):
        virtual_id = id - 1
        self.players[virtual_id] = Player(virtual_id, position)

    def do_turn(self):
        cur_player = self.players[self.cur_virtual_player_id]
        cur_player.do_turn(self.dice)
        self.cur_virtual_player_id = (self.cur_virtual_player_id + 1) % NUM_PLAYERS
        return cur_player


class Player:
    def __init__(self, virtual_id, position):
        self.virtual_id = virtual_id
        self.virtual_position = position - 1
        self.score = 0

    def do_turn(self, dice):
        total = 0
        for i in range(3):
            total += dice.roll()
        self.virtual_position = (self.virtual_position + total) % NUM_POSITIONS
        self.score += self.virtual_position + 1

    def do_full_turn(self, value):
        self.virtual_position += value
        if self.virtual_position >= NUM_POSITIONS:
            self.virtual_position -= NUM_POSITIONS
        self.score += self.virtual_position + 1


class DeterministicDice:
    def __init__(self):
        self.value = 0
        self.num_rolls = 0

    def roll(self):
        self.value += 1
        self.num_rolls += 1
        return self.value


"""
7 branches per turn
turn values:
3 (111)
4 (112, 121, 211)
5 (113, 131, 311, 122, 212, 221)
6 (123, 132, 231, 213, 312, 321, 222)
7 (322, 232, 223, 331, 313, 133)
8 (332, 323, 233)
9 (333)
"""

TURN_VALUES = [3, 4, 5, 6, 7, 8, 9]
TURN_VALUE_WEIGHT = {
    3: 1,
    4: 3,
    5: 6,
    6: 7,
    7: 6,
    8: 3,
    9: 1
}

class TurnNode:
    def __init__(self, weight, p1, p2):
        self.weight = weight
        self.p1 = p1
        self.p2 = p2
