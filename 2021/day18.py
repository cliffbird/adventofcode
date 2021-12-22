from collections import Counter
from copy import copy, deepcopy
from main import BaseProcessor
from math import ceil, floor
from queue import SimpleQueue
import sys
from threading import Thread, Lock


class D18Processor(BaseProcessor):

    def setup(self):
        string = ""
        with open(self.path, "r") as f:
            for y, line in enumerate(f):
                line = line.strip()
                string += line

        self.snails = make_snails(string)
        """
        for snail in self.snails:
            print("before: " + snail.get_print_output())
            snail.reduce()
            print("after: " + snail.get_print_output())
            print()
        """

    def run1(self):
        self.setup()

        final_snail = self.snails[0]
        for snail in self.snails[1:]:
            temp = add_snails(final_snail, snail)
            final_snail = temp
        final_snail.reduce()

        #print("sum: " + final_snail.get_print_output())
        print(f"part1: {final_snail.get_magnitude()}")

    def run2(self):
        largest_mag = 0
        for i, snail in enumerate(self.snails):
            rest = []
            rest.extend(self.snails[:i])
            rest.extend(self.snails[i+1:])

            for other_snail in rest:
                temp = add_snails(snail, other_snail)
                mag = temp.get_magnitude()
                if mag > largest_mag:
                    largest_mag = mag
        print(f"part2: {largest_mag}")


def make_snails(string):
    prev_char = None
    snails = []
    snail_history = []
    depth = -1
    for i, char in enumerate(string):
        if char == '[':
            depth += 1
            snail = Snail()
            snail.depth = depth
            if snail_history:
                snail.parent = snail_history[-1]
                if snail.parent.left is None:
                    snail.parent.left = snail
                else:
                    assert snail.parent.right is None
                    snail.parent.right = snail
            snail_history.append(snail)
        elif char >= '0' and char <= '9':
            value = int(char)
            if prev_char == '[':
                snail_history[-1].left = value
            elif prev_char == ',':
                snail_history[-1].right = value
        elif char == ']':
            last_snail = snail_history.pop()
            depth -= 1
            if not snail_history:
                assert depth == -1
                snails.append(last_snail)
        prev_char = char
    return snails

def add_snails(s1, s2):
    snail = Snail()
    snail.left = deepcopy(s1)
    snail.left.parent = snail
    snail.right = deepcopy(s2)
    snail.right.parent = snail
    snail.depth = 0
    snail.reduce()
    return snail


class Snail:
    def __init__(self):
        self.left = None
        self.right = None
        self.depth = None
        self.parent = None

    def print(self):
        print(self.get_print_output())

    def __repr__(self):
        return self.get_print_output()

    def get_print_output(self):
        output = "["
        if isinstance(self.left, Snail):
            output += self.left.get_print_output()
        else:
            output += str(self.left)
        output += ","
        if isinstance(self.right, Snail):
            output += self.right.get_print_output()
        else:
            output += str(self.right)
        output += "]"
        return output

    def reduce(self):
        assert self.parent is None

        # Set depths
        self.set_depths(0)
        while True:
            while True:
                next_to_explode = self.find_next_to_explode()
                if next_to_explode:
                    next_to_explode.explode()
                else:
                    break

            next_to_split = self.find_next_to_split()
            if next_to_split:
                next_to_split.split()
            else:
                break

    def set_depths(self, depth):
        if depth > 0:
            assert self.parent is not None
        self.depth = depth
        if isinstance(self.left, Snail):
            self.left.set_depths(depth + 1)
        if isinstance(self.right, Snail):
            self.right.set_depths(depth + 1)

    def find_next_to_explode(self):
        if self.depth >= 4 and isinstance(self.left, int) and isinstance(self.right, int):
            return self
        if isinstance(self.left, Snail):
            cur = self.left.find_next_to_explode()
            if cur:
                return cur
        if isinstance(self.right, Snail):
            cur = self.right.find_next_to_explode()
            if cur:
                return cur
        return None

    def explode(self):
        assert self.depth >= 4
        assert self.parent is not None
        assert isinstance(self.left, int)
        assert isinstance(self.right, int)

        first_regular_lefts_parent, use_left = self.get_first_regular_lefts_parent()
        if first_regular_lefts_parent:
            if use_left:
                first_regular_lefts_parent.left += self.left
            else:
                first_regular_lefts_parent.right += self.left

        first_regular_rights_parent, use_right = self.get_first_regular_rights_parent()
        if first_regular_rights_parent:
            if use_right:
                first_regular_rights_parent.right += self.right
            else:
                first_regular_rights_parent.left += self.right

        if self == self.parent.left:
            self.parent.left = 0
        else:
            self.parent.right = 0

        self.depth = None
        self.left = None
        self.right = None

    def get_first_regular_lefts_parent(self):
        # search up
        cur = self
        while cur.parent is not None:
            # search up until cur is a right (therefore there is something on the left)
            if cur == cur.parent.right:
                # Found a "left"
                cur = cur.parent
                if isinstance(cur.left, Snail):
                    return cur.left.get_rightmost_values_parent(), False
                else:
                    return cur, True
            else:
                cur = cur.parent
        return None, False

    def get_first_regular_rights_parent(self):
        cur = self
        while cur.parent is not None:
            # search up until cur is a left (therefore there is something on the right)
            if cur == cur.parent.left:
                # Found a "right"
                cur = cur.parent
                if isinstance(cur.right, Snail):
                    return cur.right.get_leftmost_values_parent(), False
                else:
                    return cur, True
            else:
                cur = cur.parent
        return None, False

    def get_rightmost_values_parent(self):
        # starting at the current snail, keep going down-right until a value
        cur = self
        while isinstance(cur, Snail):
            last_parent = cur
            cur = cur.right
        return last_parent

    def get_leftmost_values_parent(self):
        # starting at the current snail, keep going down-left until a value
        cur = self
        while isinstance(cur, Snail):
            last_parent = cur
            cur = cur.left
        return last_parent

    def find_next_to_split(self):
        if isinstance(self.left, Snail):
            cur = self.left.find_next_to_split()
            if cur:
                return cur
        elif self.left >= 10:
            return self
        if isinstance(self.right, Snail):
            cur = self.right.find_next_to_split()
            if cur:
                return cur
        elif self.right >= 10:
            return self
        return None

    def split(self):
        if isinstance(self.left, int) and self.left >= 10:
            new_snail = Snail()
            new_snail.left = floor(self.left/2)
            new_snail.right = ceil(self.left / 2)
            new_snail.depth = self.depth + 1
            new_snail.parent = self
            self.left = new_snail
        elif isinstance(self.right, int) and self.right >= 10:
            new_snail = Snail()
            new_snail.left = floor(self.right/2)
            new_snail.right = ceil(self.right/2)
            new_snail.depth = self.depth + 1
            new_snail.parent = self
            self.right = new_snail

    def get_magnitude(self):
        magnitude = 0
        if isinstance(self.left, Snail):
            magnitude += 3 * self.left.get_magnitude()
        else:
            magnitude += 3 * self.left
        if isinstance(self.right, Snail):
            magnitude += 2 * self.right.get_magnitude()
        else:
            magnitude += 2 * self.right
        return magnitude
