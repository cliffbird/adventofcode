from main import BaseProcessor


class D2Processor(BaseProcessor):
    def run1(self):
        self.parse_valid()

    def parse_valid(self):
        valid_count = 0
        with open(self.path, "r") as f:
            for line in f:
                min_max, letter_colon, word = line.split()
                min, max = min_max.split("-")
                min = int(min)
                max = int(max)

                letter = letter_colon[:-1]
                letter_count = 0
                for index in range(len(word)):
                    char = word[index]
                    if char == letter:
                        letter_count += 1
                if letter_count >= min and letter_count <= max:
                    valid_count += 1

        print(f"part1 num valid: {valid_count}")

    def run2(self):
        self.parse_valid2()

    def parse_valid2(self):
        valid_count = 0
        with open(self.path, "r") as f:
            for line in f:
                min_max, letter_colon, word = line.split()
                min, max = min_max.split("-")
                min = int(min)
                max = int(max)

                letter = letter_colon[:-1]
                num_matches = 0
                if word[min-1] == letter:
                    num_matches += 1
                if word[max-1] == letter:
                    num_matches += 1
                if num_matches == 1:
                    valid_count += 1

        print(f"part2 num valid: {valid_count}")