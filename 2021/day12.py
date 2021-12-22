from collections import Counter
from copy import copy
from main import BaseProcessor


class D12Processor(BaseProcessor):

    def setup(self):
        self.caves = Caves()
        with open(self.path, "r") as f:
            for i, line in enumerate(f):
                line = line.strip()
                name1, name2 = line.split("-")
                self.caves.add_path(name1, name2)

        for small_cave in self.caves.small_caves:
            small_cave.max_visits = 1
        self.caves.process_paths()
        print(f"part1: {len(self.caves.paths)}")

        start_cave = self.caves.caves["start"]
        end_cave = self.caves.caves["end"]
        self.caves.small_caves.remove(start_cave)
        self.caves.small_caves.remove(end_cave)
        unique_path_strings = set()
        for i, small_cave in enumerate(self.caves.small_caves):
            small_cave.max_visits = 2
            self.caves.process_paths()
            small_cave.max_visits = 1

            for path in self.caves.paths:
                output = path.get_print()
                unique_path_strings.add(output)

        #for path in unique_path_strings:
        #    print(path)
        print(f"part2: {len(unique_path_strings)}")


    def process(self, line_number, line):
        pass

    def run1(self):
        self.setup()

    def run2(self):
        pass


class Caves:
    def __init__(self):
        self.start = Cave("start")
        self.end = Cave("end")
        self.caves = {}
        self.small_caves = []

    def add_path(self, name1, name2):
        c1 = None
        if name1 not in self.caves:
            self.caves[name1] = Cave(name1)
        c1 = self.caves[name1]
        if name2 not in self.caves:
            self.caves[name2] = Cave(name2)
        c2 = self.caves[name2]

        if c1.is_small and c1 not in self.small_caves:
            self.small_caves.append(c1)
        if c2.is_small and c2 not in self.small_caves:
            self.small_caves.append(c2)

        c1.add_neighbor(c2)
        c2.add_neighbor(c1)

    def process_paths(self):
        self.paths = []
        cur_path = Path()
        cur_path.append(self.caves["start"])
        pending_paths = []
        pending_paths.append(cur_path)
        while pending_paths:
            pending_paths_copy = copy(pending_paths)
            pending_paths = []
            for pending_path in pending_paths_copy:
                cur_cave = pending_path.get_cur_cave()
                for neighbor in cur_cave.neighbors:
                    new_path = copy(pending_path)
                    if new_path.append(neighbor):
                        # Added
                        if neighbor.name == "end":
                            self.paths.append(new_path)
                        else:
                            pending_paths.append(new_path)


class Cave:
    def __init__(self, name):
        self.neighbors = set()
        self.name = name
        self.is_small = name[0].islower()
        self.is_large = not self.is_small
        self.max_visits = -1

    def add_neighbor(self, neighbor):
        self.neighbors.add(neighbor)


class Path:
    def __init__(self):
        self.entries = set()
        self.path = []

    def append(self, cave):
        if cave not in self.entries or cave.is_large or \
           (self.get_num_occurrences(cave) < cave.max_visits):
            self.path.append(cave)
            self.entries.add(cave)
            return True
        return False

    def get_num_occurrences(self, cur_cave):
        count = 0
        for cave in self.path:
            if cave == cur_cave:
                count += 1
        return count

    def get_cur_cave(self):
        return self.path[-1]

    def __copy__(self):
        new_path = Path()
        new_path.entries = copy(self.entries)
        new_path.path = copy(self.path)
        return new_path

    def get_print(self):
        output = ""
        for cave in self.path[:-1]:
            output += f"{cave.name},"
        output += self.path[-1].name
        return output

    def print(self):
        print(self.get_print())
