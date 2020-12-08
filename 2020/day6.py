from main import BaseProcessor


class D6Processor(BaseProcessor):
    def run1(self):
        groups = []
        group = set()
        with open(self.path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    groups.append(group)
                    group = set()
                else:
                    for index in range(len(line)):
                        char = line[index]
                        group.add(char)
        groups.append(group)

        sum = 0
        for group in groups:
            sum += len(group)
        print(f"sum: {sum}")

    def run2(self):
        groups = []
        group = None
        with open(self.path, "r") as f:
            for line in f:
                line = line.strip()
                if not line:
                    groups.append(group)
                    group = None
                else:
                    if group is not None:
                        to_remove = set()
                        for char in group:
                            if char not in line:
                                to_remove.add(char)
                        for char in to_remove:
                            group.remove(char)
                    else:
                        group = set()
                        for index in range(len(line)):
                            char = line[index]
                            group.add(char)
        groups.append(group)

        sum = 0
        for group in groups:
            sum += len(group)
        print(f"sum: {sum}")