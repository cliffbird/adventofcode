from main import BaseProcessor


class D3Processor(BaseProcessor):
    def run1(self):
        self.traverse(3, 1)

    def traverse(self, col_shift=1, row_shift=3):
        num_trees = 0
        row = 0
        col = 0
        with open(self.path, "r") as f:
            for line in f:
                if not row % row_shift:
                    char = line[col]
                    if char != '.':
                        num_trees += 1

                    col += col_shift
                    col = col % len(line.strip())

                row += 1

        print(f"right {col_shift}, down {row_shift}, num trees: {num_trees}")
        return num_trees

    def run2(self):
        v1 = self.traverse(1, 1)
        v2 = self.traverse(3, 1)
        v3 = self.traverse(5, 1)
        v4 = self.traverse(7, 1)
        v5 = self.traverse(1, 2)
        ans = v1*v2*v3*v4*v5
        print(f"{v1}*{v2}*{v3}*{v4}*{v5} = {ans}")