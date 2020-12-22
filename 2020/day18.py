from main import BaseProcessor

class D18Processor(BaseProcessor):
    def run_all(self):
        self.base_run(path_suffix="example")
        self.base_run(path_suffix="example2")
        self.base_run(path_suffix="example3")
        self.base_run(path_suffix="example4")
        self.base_run(path_suffix="example5")
        self.base_run(path_suffix="example6")
        self.base_run()

    def run1(self):
        with open(self.path, "r") as f:
            sum = 0
            for line in f:
                line = line.strip()
                line = line.replace("(", "( ")
                line = line.replace(")", " )")
                answer = self.calculate(line.split())
                sum += answer
        print(f"part1: {sum}")

    def calculate(self, parts):
        lparenthesis_index_stack = []  # stack of left paranthesis

        prev_op = "+"
        cur = 0
        for index in range(len(parts)):
            part = parts[index]

            if part == "(":
                lparenthesis_index_stack.append(index)
            elif part == ")":
                lparenthesis_index = lparenthesis_index_stack.pop()
                if lparenthesis_index_stack:
                    continue

                parenthesis_total = self.calculate(parts[lparenthesis_index+1:index])

                if prev_op == "+":
                    cur += parenthesis_total
                elif prev_op == "*":
                    cur *= parenthesis_total
                else:
                    raise Exception(f"Invalid prev_op: {prev_op}")
                prev_op = None
            elif lparenthesis_index_stack:
                continue
            elif part == "+" or part == "*":
                prev_op = part
            else:
                value = int(part)

                assert prev_op is not None
                if prev_op == "+":
                    cur += value
                elif prev_op == "*":
                    cur *= value
                else:
                    raise Exception(f"Invalid prev_op: {prev_op}")
        return cur

    def run2(self):
        with open(self.path, "r") as f:
            sum = 0
            for line in f:
                line = line.strip()
                line = line.replace("(", "( ")
                line = line.replace(")", " )")
                answer = self.calculate2(line.split())
                sum += answer
        print(f"part2: {sum}")

    def calculate2(self, parts):
        parts = self.reduce_parenthesis(parts)
        assert not self.has_parenthesis(parts)
        return self.calculate_no_parenthesis(parts)

    def has_parenthesis(self, parts):
        has = False
        for part in parts:
            if part == "(":
                has = True
                break
        return has

    def reduce_parenthesis(self, parts):
        new_parts = []
        lparenthesis_index_stack = []  # stack of left paranthesis
        for index in range(len(parts)):
            part = parts[index]

            if part == "(":
                lparenthesis_index_stack.append(index)
            elif part == ")":
                lparenthesis_index = lparenthesis_index_stack.pop()
                if lparenthesis_index_stack:
                    continue

                sub_parts = parts[lparenthesis_index + 1:index]
                new_parts.append(self.calculate2(sub_parts))
            elif lparenthesis_index_stack:
                continue
            else:
                new_parts.append(part)
        return new_parts

    def calculate_no_parenthesis(self, parts):
        cur = None
        prev_op = None
        prev_value = None
        for index in range(len(parts)):
            part = parts[index]
            if part == "+" or part == "*":
                prev_op = part
            else:
                value = int(part)

                if prev_op is None:
                    cur = value
                elif prev_op == "+":
                    if prev_value:
                        prev_value += value
                    else:
                        cur += value
                elif prev_op == "*":
                    if prev_value:
                        cur *= prev_value
                    prev_value = value
                else:
                    raise Exception(f"Invalid prev_op: {prev_op}")
        if prev_value:
            cur *= prev_value
        return cur
