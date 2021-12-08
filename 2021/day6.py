from copy import copy
from main import BaseProcessor

class D6Processor(BaseProcessor):

    def setup(self):
        self.tank = set()
        with open(self.path, "r") as f:
            for line in f:
                line = line.strip()
                ages = line.split(",")
                for age in ages:
                    self.tank.add(Fish(int(age), self.tank))

    def run1(self):
        pass
        self.setup()

        for i in range(80):
            num_to_add = 0
            for fish in self.tank:
                if fish.do_day():
                    num_to_add += 1
            for j in range(num_to_add):
                self.tank.add(Fish(8, self.tank))
        print(f"part1: {len(self.tank)}")


    def run2(self):
        age_counts = []
        for i in range(9):
            age_counts.append(0)

        with open(self.path, "r") as f:
            for line in f:
                line = line.strip()
                ages = line.split(",")
                for age in ages:
                    age_counts[int(age)] += 1

        for i in range(256):
            age_counts = do_day(age_counts)
            if i == 79:
                print(f"part1: {sum(age_counts)}")
        print(f"part2: {sum(age_counts)}")

def do_day(day):
    old_day0 = int(day[0])

    day[0] = int(day[1])
    day[1] = int(day[2])
    day[2] = int(day[3])
    day[3] = int(day[4])
    day[4] = int(day[5])
    day[5] = int(day[6])
    day[6] = old_day0 + int(day[7])
    day[7] = int(day[8])
    day[8] = old_day0
    return day


class Fish:
    def __init__(self, age, tank):
        self.age = age
        self.tank = tank

    def do_day(self):
        self.age -= 1
        if self.age == -1:
            self.age = 6
            return True
        return False
