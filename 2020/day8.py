import copy
from main import BaseProcessor


class D8Processor(BaseProcessor):
    def run1(self):
        bios = BIOS()
        bios.store(self.path)
        success = bios.run()
        print(f"Run status={success}, acc={bios.acc}")

    def run2(self):
        bios = BIOS()
        bios.store(self.path)
        bios_original = copy.deepcopy(bios.code)
        pc = -1
        for instruction in bios.code:
            pc += 1
            cmd = instruction[0]
            value = instruction[1]

            if cmd == "jmp":
                bios.code[pc] = ("nop", value)
            elif cmd == "nop":
                bios.code[pc] = ("jmp", value)
            else:
                continue

            success = bios.run()

            if success:
                print(f"Run status={success}, acc={bios.acc}")
                return
            else:
                bios.code = copy.deepcopy(bios_original)


class BIOS:
    def __init__(self):
        self.pc = 0
        self.acc = 0
        self.code = []
        self.history_set = set()

    def store(self, path):
        # store the code
        with open(path, "r") as f:
            for line in f:
                line = line.strip()
                cmd, value_str = line.split()
                value = int(value_str)
                self.code.append((cmd, value))

    def run(self):
        self.pc = 0
        self.acc = 0
        self.history_set = set()
        while self.pc < len(self.code):
            if self.pc in self.history_set:
                return False
            cmd, value = self.code[self.pc]

            self.history_set.add(self.pc)

            if cmd == "acc":
                self.do_acc(value)
            elif cmd == "jmp":
                self.do_jmp(value)
            elif cmd == "nop":
                self.do_nop(value)

        return True

    def do_acc(self, value):
        self.acc += value
        self.pc += 1

    def do_jmp(self, value):
        self.pc += value

    def do_nop(self, value):
        self.pc += 1
