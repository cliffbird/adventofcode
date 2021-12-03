from main import BaseProcessor

class D1Processor(BaseProcessor):

    def run1(self):
        with open(self.path, "r") as f:
            prev_value = None
            num_increases = 0
            for line in f.readlines():
                line = line.strip()
                value = int(line)
                if prev_value:
                    if value > prev_value:
                        num_increases += 1
                prev_value = value

            print(f"part1: {num_increases}")

    def run2(self):
        with open(self.path, "r") as f:
            windows = []
            cur = [[], [], []]
            prev_value = None
            for line in f.readlines():
                line = line.strip()
                value = int(line)
                add_to_cur(cur, value, windows)

            num_increases = 0
            values = []
            for window in windows:
                values.append(sum(window))

            prev_value = None
            for value in values:
                if prev_value:
                    if value > prev_value:
                        num_increases += 1
                prev_value = value
            print(f"part2: {num_increases}")

def add_to_cur(cur, value, windows):
    prev_len = None
    for window in cur:
        cur_len = len(window)
        if len(window) < 3 and (prev_len is None  or (prev_len is not None and cur_len != prev_len)):
            window.append(value)
            if len(window) == 3:
                windows.append(list(window))
                window.clear()
        prev_len = cur_len
