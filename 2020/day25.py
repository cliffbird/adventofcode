from copy import deepcopy
from main import BaseProcessor
import re

class D25Processor(BaseProcessor):
    def run_all(self):
        self.base_run(path_suffix="example")
        self.base_run()

    def run1(self):
        public_keys = set()
        with open(self.path, "r") as f:
            for line in f:
                line = line.strip()
                public_keys.add(int(line))

        found_loop_counts = {}
        b = Base(7)
        loop_count = 0
        while len(found_loop_counts) != len(public_keys):
            loop_count += 1
            value = b.run_loop()
            if value in public_keys:
                found_loop_counts[value] = loop_count

        encryption_keys = set()
        for public_key in public_keys:
            b = Base(public_key)
            other_keys = set(public_keys)
            other_keys.remove(public_key)
            for other_key in other_keys:
                ek = b.run_loops(found_loop_counts[other_key])
                break
            if encryption_keys:
                assert ek in encryption_keys
            else:
                encryption_keys.add(ek)

        print(f"part1: {ek}")

    def run2(self):
        with open(self.path, "r") as f:
            for line in f:
                line = line.strip()
        print(f"part2: ")


class Base:
    def __init__(self, subject_number):
        self.subject_number = subject_number
        self.value = 1

    def run_loops(self, loop_count):
        for i in range(loop_count):
            self.run_loop()
        return self.value


    def run_loop(self):
        self.value *= self.subject_number
        self.value %= 20201227
        return self.value

    def reverse_loop(self, public_key):
        pass

    def reset(self):
        self.value = 1