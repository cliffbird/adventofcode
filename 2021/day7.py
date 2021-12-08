from collections import Counter
from copy import copy
from main import BaseProcessor

class D7Processor(BaseProcessor):

    def setup(self):
        positions = []
        self.min = 1000
        self.max = 0
        with open(self.path, "r") as f:
            for line in f:
                for position in line.strip().split(","):
                    value = int(position)
                    if value < self.min:
                        self.min = value
                    if value > self.max:
                        self.max = value
                    positions.append(value)
                break
        self.positions = positions

    def run1(self):
        self.setup()
        least = None
        for value in range(self.min, self.max):
            total = 0
            for position in self.positions:
                total += abs(position - value)
            if least is None or total < least[0]:
                least = (total, value)
        print(f"part1: least: {least[0]} at {least[1]}")


    def run2(self):
        self.setup()
        least = None
        sums = {}
        for value in range(self.min, self.max):
            total = 0
            for position in self.positions:
                distance = abs(position - value)
                if distance not in sums:
                    sum = 0
                    for i in range(distance):
                        sum += i + 1
                    sums[distance] = sum

                total += sums[distance]
            if least is None or total < least[0]:
                least = (total, value)
        print(f"part2: least: {least[0]} at {least[1]}")
