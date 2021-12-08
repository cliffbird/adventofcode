from main import BaseProcessor
import re

class D23Processor(BaseProcessor):
    def run_all(self):
        self.base_run(path_suffix="example")
        self.base_run()

    def run1(self):
        with open(self.path, "r") as f:
            for line in f:
                line = line.strip()
                g = Game(line)

        g.verify_links()

        for move in range(1,10+1):
            g.play(move)

        g.print_cups()


        print("-- final --")
        print(f"part1: 10: {g.get_final()}")

        for move in range(11,100+1):
            g.play(move)
        print("-- final --")
        print(f"part1: 100: {g.get_final()}")


    def run2(self):
        with open(self.path, "r") as f:
            for line in f:
                line = line.strip()
                g = Game(line, enable_print=False)
        g.verify_links()

        value = g.max + 1
        while g.num_cups < 1000000:
            prev = g.cur_cup.prev
            new_cup = Cup(value)
            prev.next = new_cup
            new_cup.prev = prev
            new_cup.next = g.cur_cup

            g.cur_cup.prev = new_cup
            g.max = value
            g.num_cups += 1
            value += 1
        g.verify_links()

        for move in range(1,10000000+1):
            g.play(move)

        after_one_cup = None
        cur_cup = g.cur_cup
        for i in range(g.num_cups):
            if cur_cup.value == 1:
                after_one_cup = cur_cup.next
                break
            cur_cup = cur_cup.next

        print("-- final --")
        product = after_one_cup.value* after_one_cup.next.value
        print(f"part2: {after_one_cup.value} * {after_one_cup.next.value} = {product}")

class Game:
    def __init__(self, cups_initial, enable_print=True):
        self.set_initial_cups(cups_initial)
        self.enable_print = enable_print
        self.value_dict = {}

    def set_initial_cups(self, cups_initial):
        self.cur_cup = None
        self.num_cups = len(cups_initial)
        self.max = 0
        prev = None
        for char in cups_initial:
            value = int(char)
            if value > self.max:
                self.max = value
            cup = Cup(value)
            if prev is None:
                self.cur_cup = cup
            else:
                cup.prev = prev
                prev.next = cup
            prev = cup
        cup.next = self.cur_cup
        self.cur_cup.prev = cup

        cur_cup = self.cur_cup

        self.min = self.max
        for i in range(self.num_cups):
            value = cur_cup.value
            if value < self.min:
                self.min = value
            cur_cup = cur_cup.next

    def verify_links(self):
        cur_cup = self.cur_cup
        values = set()
        for i in range(self.num_cups):
            values.add(cur_cup.value)
            self.value_dict[cur_cup.value] = cur_cup
            assert cur_cup.next is not None and cur_cup.prev is not None
            cur_cup = cur_cup.next
        assert cur_cup == self.cur_cup

        for i in range(1,self.num_cups+1):
            assert i in values

    def play(self, move):
        if self.enable_print:
            print(f"-- move {move} --")
        current_value = self.cur_cup.value
        if self.enable_print:
            self.print_cups()

        # unlink pickup
        pickup = set()
        pickup_cup_start = self.cur_cup.next
        cur_cup = pickup_cup_start
        for i in range(3):
            pickup.add(cur_cup.value)
            cur_cup = cur_cup.next
        pickup_cup_end = cur_cup.prev

        pickup_cup_start.prev = pickup_cup_end
        pickup_cup_end.next = pickup_cup_start

        self.cur_cup.next = cur_cup
        cur_cup.prev = self.cur_cup

        if self.enable_print:
            print("pick up: ", end="")
            self.print_cup_link(pickup_cup_start)
            print()

        # determine the destination of the pickup
        destination_value = self.cur_cup.value - 1
        if destination_value < self.min:
            destination_value = self.max
        while destination_value in pickup:
            destination_value -= 1
            if destination_value < self.min:
                destination_value = self.max
        if self.enable_print:
            print(f"destination: {destination_value}")
        # find the destination cup
        destination_cup = self.value_dict[destination_value]
        after_destination_cup = destination_cup.next

        # insert the pickup
        destination_cup.next = pickup_cup_start
        pickup_cup_start.prev = destination_cup

        pickup_cup_end.next = after_destination_cup
        after_destination_cup.prev = pickup_cup_end
        self.cur_cup = self.cur_cup.next

    def play_orig(self, move):
        if self.enable_print:
            print(f"-- move {move} --")
        current_value = self.cups[self.cur]
        if self.enable_print:
            self.print_cups()

        pickup = []
        if self.enable_print:
            print("pick up: ", end="")
        cur_index = (self.cur + 1)%len(self.cups)
        for i in range(3):
            cur_index = cur_index%len(self.cups)
            value = self.cups.pop(cur_index)
            pickup.append(value)
            if self.enable_print:
                print(f"{value} ", end="")
        if self.enable_print:
            print()

        self.cur = self.cups.index(current_value)

        # determine the destination of the pickup
        destination_value = self.cups[self.cur] - 1
        if destination_value < self.min:
            destination_value = self.max
        while destination_value in pickup:
            destination_value -= 1
            if destination_value < self.min:
                destination_value = self.max
        if self.enable_print:
            print(f"destination: {destination_value}")
        destination_index = self.cups.index(destination_value)

        insert_index = (destination_index + 1)%len(self.cups)
        for value in pickup:
            self.cups.insert(insert_index, value)
            insert_index = (insert_index + 1)%len(self.cups)
        if self.enable_print:
            print()

        self.cur = (self.cups.index(current_value) + 1)%len(self.cups)

    def print_cups(self):
        print("cups: ", end="")
        cur_cup = self.cur_cup
        print(f"({cur_cup.value}) ", end="")
        cur_cup = cur_cup.next
        for i in range(self.num_cups-1):
            print(f"{cur_cup.value} ", end="")
            cur_cup = cur_cup.next
        print()

    def print_cup_link(self, start_cup):
        cur_cup = start_cup
        print(f"{cur_cup.value} ", end="")
        cur_cup = cur_cup.next
        while cur_cup != start_cup:
            print(f"{cur_cup.value} ", end="")
            cur_cup = cur_cup.next

    def get_final(self):
        after_one_cup = None
        cur_cup = self.cur_cup
        for i in range(self.num_cups):
            if cur_cup.value == 1:
                after_one_cup = cur_cup.next
                break
            cur_cup = cur_cup.next

        output = ""
        cur_cup = after_one_cup
        for i in range(self.num_cups - 1):
            output += f"{cur_cup.value}"
            cur_cup = cur_cup.next
        return output



class Cup:
    def __init__(self, value):
        self.value = value
        self.prev = None
        self.next = None
