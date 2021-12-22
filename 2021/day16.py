from collections import Counter
from copy import copy, deepcopy
from main import BaseProcessor
from queue import SimpleQueue
import sys
from threading import Thread, Lock


class D16Processor(BaseProcessor):

    def setup(self):
        hex = ""
        if "example" not in self.path:
            pass
        with open(self.path, "r") as f:
            rows = []
            for y, line in enumerate(f):
                row = []
                line = line.strip()
                if line:
                    hex = line

        bin = convert_to_bin(hex)

        self.p = Processor(bin)
        value = self.p.process()
        print(f"part1: {self.p.version_sum}")
        print(f"part2: {value}")


    def run1(self):
        self.setup()


    def run2(self):
        pass

OP_MAP = {
    "version": {
        "next": "type_id"
    },
    "type_id": {
        "next": "pad4"
    },
    "pad4": 0
}

class Processor:
    def __init__(self, bin):
        self.bin = bin
        self.bin_position = 0
        self.version_sum = 0

    def process(self):
        type_id = self.process_header()
        if type_id == 4:
            value = self.get_literal_value()
            return value
        else:
            # operator packet
            values = self.process_operator()
            if type_id == 0:
                return sum(values)
            elif type_id == 1:
                product = 1
                for value in values:
                    product *= value
                return product
            elif type_id == 2:
                return min(values)
            elif type_id == 3:
                return max(values)
            elif type_id == 5:
                if values[0] > values[1]:
                    return 1
                return 0
            elif type_id == 6:
                if values[0] < values[1]:
                    return 1
                return 0
            elif type_id == 7:
                if values[0] == values[1]:
                    return 1
                return 0
            else:
                print(f"ERROR: invalid type_id: {self.type_id}")


    def process_header(self):
        start_bin_position = self.bin_position
        end_bin_position = self.bin_position + 3
        value_str = self.bin[start_bin_position:end_bin_position]
        self.bin_position = end_bin_position

        self.version = convert_bin_to_int(value_str)
        self.version_sum += self.version

        start_bin_position = self.bin_position
        end_bin_position = self.bin_position + 3
        value_str = self.bin[start_bin_position:end_bin_position]
        self.bin_position = end_bin_position

        type_id = convert_bin_to_int(value_str)
        return type_id

    def get_literal_value(self):
        # read groups of 4-bits until leading bit is a 0, that is the last one
        # NOTE: first group may be padded with 0 so ignore that
        value = 0
        end_loop = False
        while not end_loop:
            end_loop_char = self.bin[self.bin_position]
            self.bin_position += 1
            if end_loop_char == "0":
                end_loop = True

            start_bin_position = self.bin_position
            end_bin_position = self.bin_position + 4
            value_str = self.bin[start_bin_position:end_bin_position]
            self.bin_position = end_bin_position

            value *= 16
            value += convert_bin_to_int(value_str)

        print(f"literal: {value}")

        return value

    def process_operator(self):
        length_type_id = self.bin[self.bin_position]
        self.bin_position += 1
        if length_type_id == "0":
            length = 15
        else:
            length = 11
        start = self.bin_position
        end = self.bin_position + length
        self.bin_position = end
        value_str = self.bin[start:end]
        value = convert_bin_to_int(value_str)
        if length_type_id == "0":
            sub_length = value

            values = self.process_unknown(sub_length)
        else:
            num_subs = value
            values = self.process_subs(num_subs)

        return values

    def process_unknown(self, num_bits):
        start = self.bin_position

        values = []
        while self.bin_position - start < num_bits:
            value = self.process()
            values.append(value)
        return values

    def process_subs(self, num_subs):
        values = []
        for i in range(num_subs):
            value = self.process()
            values.append(value)
        return values




def convert_to_bin(hex):
    bin = ""
    for char in hex:
        bin += hex2bin(char)
    return bin

def convert_bin_to_int(bin):
    value = 0
    for char in bin:
        value *= 2
        if char == "1":
            value += 1
    return value

def hex2bin(char):
    if char == "0":
        return "0000"
    elif char == "1":
        return "0001"
    elif char == "2":
        return "0010"
    elif char == "3":
        return "0011"
    elif char == "4":
        return "0100"
    elif char == "5":
        return "0101"
    elif char == "6":
        return "0110"
    elif char == "7":
        return "0111"
    elif char == "8":
        return "1000"
    elif char == "9":
        return "1001"
    elif char == "A":
        return "1010"
    elif char == "B":
        return "1011"
    elif char == "C":
        return "1100"
    elif char == "D":
        return "1101"
    elif char == "E":
        return "1110"
    elif char == "F":
        return "1111"

