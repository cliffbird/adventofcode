from main import BaseProcessor


class D1Processor(BaseProcessor):
    SUM = 2020
    EQUAL_POINT = 1010

    def run1(self):
        self.init()
        self.do_double()

    def run2(self):
        self.init()
        self.do_triple()

    def init(self):
        data_list = []
        with open(self.path, "r") as f:
            for line in f:
                data_list.append(int(line.strip()))

        self.data_list = data_list
        self.data_list.sort()

    def do_double(self):
        lower = set()
        upper = set()
        equal = []

        for value in self.data_list:
            if value < self.EQUAL_POINT:
                lower.add(value)
            elif value > self.EQUAL_POINT:
                upper.add(value)
            else:
                equal.append(value)

        if len(equal) > 1:
            print(f"Multiple {self.EQUAL_POINT} found: {self.EQUAL_POINT*self.EQUAL_POINT}")

        for value in lower:
            difference = self.SUM - value
            if difference in upper:
                answer = value * difference
                print(f"{value} * {difference} = {answer}")

    def do_triple(self):
        for i1 in range(len(self.data_list)):
            v1 = self.data_list[i1]
            for i2 in range(len(self.data_list)):
                if i1 == i2:
                    continue
                v2 = self.data_list[i2]
                difference = self.SUM - v1 - v2
                if difference < 0:
                    break
                # binary search difference
                i3 = self.get_value_index(difference)
                if i3:
                    v3 = self.data_list[i3]
                    answer = v1*v2*v3
                    print(f"{v1} * {v2} * {v3}= {answer}")

    def get_value_index(self, find_value):
        index = int(len(self.data_list) / 2)
        width = index
        while True:
            cur_value = self.data_list[index]
            if cur_value == find_value:
                return index
            elif cur_value > find_value:
                # find below
                width = int(width / 2)
                new_index = index - width
                if new_index == index:
                    break
            else:
                # find above
                width = int(width / 2)
                new_index = index - width
                if new_index == index:
                    break
            index = new_index
        return None
