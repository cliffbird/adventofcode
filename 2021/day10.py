from collections import Counter
from copy import copy
from main import BaseProcessor

class D10Processor(BaseProcessor):

    def setup(self):
        self.error = []
        self.auto_complete = []
        with open(self.path, "r") as f:
            for i, line in enumerate(f):
                self.process(i, line.strip())

        points = 0
        for char in self.error:
            if char == ")":
                points += 3
            elif char == "]":
                points += 57
            elif char == "}":
                points += 1197
            elif char == ">":
                points += 25137
        print(f"part1: {points}")

        self.auto_complete.sort()
        print(f"part2: {self.auto_complete[int(len(self.auto_complete)/2)]}")


    def process(self, line_number, line):
        history = []
        for char in line:
            if char in "([{<":
                history.append(char)
            else:
                is_good = True;
                if char == ")":
                    if history[-1] != "(":
                        is_good = False
                elif char == "]":
                    if history[-1] != "[":
                        is_good = False
                elif char == "}":
                    if history[-1] != "{":
                        is_good = False
                elif char == ">":
                    if history[-1] != "<":
                        is_good = False

                if is_good:
                    history.pop(-1)
                else:
                    self.error.append(char)
                    break
        if is_good:
            auto_complete = 0
            count = len(history)
            pass
            while history:
                cur = history.pop()
                if cur == "(":
                    auto_complete = auto_complete * 5 + 1
                elif cur == "[":
                    auto_complete = auto_complete * 5 + 2
                elif cur == "{":
                    auto_complete = auto_complete * 5 + 3
                elif cur == "<":
                    auto_complete = auto_complete * 5 + 4
            self.auto_complete.append(auto_complete)

    def run1(self):
        self.setup()
        pass


    def run2(self):
        pass

