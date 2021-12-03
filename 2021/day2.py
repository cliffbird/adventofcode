from main import BaseProcessor

class D2Processor(BaseProcessor):

    def run1(self):

        with open(self.path, "r") as f:
            x = 0
            y = 0
            for line in f.readlines():
                line = line.strip()
                op, value = line.split()
                if op == "forward":
                    x += int(value)
                elif op == "down":
                    y += int(value)
                elif op == "up":
                    y -= int(value)

            print(f"part1: {x*y}")

    def run2(self):
        with open(self.path, "r") as f:
            x = 0
            y = 0
            aim = 0
            for line in f.readlines():
                line = line.strip()
                op, value = line.split()
                value = int(value)
                if op == "forward":
                    x += value
                    y += aim*value
                elif op == "down":
                    #y += value
                    aim += value
                elif op == "up":
                    #y -= value
                    aim -= value

            print(f"part2: {x * y}")