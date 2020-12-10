from main import BaseProcessor

class D10Processor(BaseProcessor):
    def run_all(self):
        self.base_run(path_suffix="example")
        self.base_run(path_suffix="example2")
        self.base_run()

    def run1(self):
        jolts = []
        with open(self.path, "r") as f:
            for line in f:
                line = line.strip()
                jolts.append(int(line))
        jolts.sort()
        prev = 0
        difference_counts = {1:0, 2:0, 3:0}
        for index in range(len(jolts)):
            next = jolts[index]
            difference = next - prev
            difference_counts[difference] += 1
            prev = next
        difference_counts[3] += 1
        print(f"part1: {difference_counts[1]} * {difference_counts[3]} = {difference_counts[1] * difference_counts[3]}")

    def run2(self):
        jolts = []
        with open(self.path, "r") as f:
            for line in f:
                line = line.strip()
                jolts.append(int(line))
        jolts.sort()
        maximum = max(jolts)

        jolts.append(maximum+3)

        self.num_branches_dict = {}

        num_branches = self.get_num_branches(0, jolts)
        print(f"part2: {num_branches}")

    def get_num_branches(self, cur, jolts):
        if cur in self.num_branches_dict:
            return self.num_branches_dict[cur]
        num_branches = 0
        if jolts:
            for index in range(len(jolts)):
                jolt = jolts[index]
                if jolt - cur <= 3:
                    num_branches += self.get_num_branches(jolt, jolts[index+1:])
                else:
                    break
            self.num_branches_dict[cur] = num_branches
            return num_branches
        else:
            if cur not in self.num_branches_dict:
                self.num_branches_dict[cur] = 1
            return 1
