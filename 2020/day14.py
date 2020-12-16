from main import BaseProcessor
import re

class D14Processor(BaseProcessor):
    def run_all(self):
        self.base_run(path_suffix="example")
        self.base_run(path_suffix="example2")
        self.base_run()

    def run1(self):
        self.value = 0
        self.memory = {}
        search = re.compile("mem\[(\d+?)\] = (\d+?)$")
        with open(self.path, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("mask"):
                    self.set_mask(line)
                elif line.startswith("mem"):
                    m = search.match(line)
                    address = int(m.group(1))
                    value = int(m.group(2))
                    result = self.apply_mask_to_value(self.bitmask_dict, value)
                    self.memory[address] = result
        memory_sum = 0
        for memory_value in self.memory.values():
            memory_sum += memory_value
        print(f"part1: {memory_sum}")

    def set_mask(self, mask_line):
        self.bitmask_str = mask_line.split()[-1]
        self.bitmask_dict = {}
        bit = 35
        for char in self.bitmask_str:
            if char == "1":
                self.bitmask_dict[bit] = 1
            elif char == "0":
                self.bitmask_dict[bit] = 0

            bit -= 1

    @classmethod
    def apply_mask_to_value(cls, bitmask_dict, value):
        result = value
        for bit, bitmask_value in bitmask_dict.items():
            if bitmask_value == 1:
                result |= (1<<bit)
            else:
                temp = ( ((1<<36)-1) ^ (1<<bit) )
                result &= temp

        return result

    def run2(self):
        if self.path_suffix == "example":
            return
        self.value = 0
        self.memory = {}
        search = re.compile("mem\[(\d+?)\] = (\d+?)$")
        with open(self.path, "r") as f:
            for line in f:
                line = line.strip()
                if line.startswith("mask"):
                    self.set_mask2(line)
                elif line.startswith("mem"):
                    m = search.match(line)
                    address = int(m.group(1))
                    value = int(m.group(2))

                    base_address = self.apply_mask_to_address(self.bitmask_dict, address)
                    addresses = self.get_floating_addresses(base_address, self.floating_bits, 0)

                    for address in addresses:
                        self.memory[address] = value
        memory_sum = 0
        for memory_value in self.memory.values():
            memory_sum += memory_value
        print(f"part2: {memory_sum}")

    @classmethod
    def get_floating_addresses(cls, base_address, floating_bits, floating_bit_index):
        return_set = set()
        if floating_bit_index >= len(floating_bits):
            return_set.add(base_address)
            return return_set
        floating_bit = floating_bits[floating_bit_index]
        first = cls.get_floating_addresses(base_address, floating_bits, floating_bit_index+1)
        for address in first:
            return_set.add(address)

        base_address2 = base_address | (1<<floating_bit)
        second = cls.get_floating_addresses(base_address2, floating_bits, floating_bit_index+1)
        for address in second:
            return_set.add(address)
        return return_set

    def apply_mask_to_address(self, bitmask_dict, value):
        result = value
        self.floating_bits = []
        for bit, bitmask_value in bitmask_dict.items():
            if bitmask_value == 1:
                result |= (1<<bit)
            elif bitmask_value is None:
                temp = (((1 << 36) - 1) ^ (1 << bit))
                result &= temp
                self.floating_bits.append(bit)
        return result

    def set_mask2(self, mask_line):
        self.bitmask_str = mask_line.split()[-1]
        self.bitmask_dict = {}
        bit = 35
        for char in self.bitmask_str:
            if char == "X":
                self.bitmask_dict[bit] = None
            elif char == "1":
                self.bitmask_dict[bit] = 1
            elif char == "0":
                self.bitmask_dict[bit] = 0

            bit -= 1