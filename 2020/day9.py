from main import BaseProcessor

class D9Processor(BaseProcessor):
    def run1(self):
        if self.path_suffix == "example":
            preamble_length = 5
        else:
            preamble_length = 25

        with open(self.path, "r") as f:
            preamble = []
            in_preamble = True
            line_number = 0
            cur_sum = 0
            for line in f:
                line = line.strip()
                if line_number >= preamble_length:
                    in_preamble = False
                line_number += 1

                cur_value = int(line)

                if in_preamble:
                    cur_sum += cur_value
                    preamble.append(cur_value)
                    continue

                # check if cur_value is a valid sum
                is_found = False
                for sub_list in self.get_valid_sums(preamble):
                    if cur_value in sub_list:
                        is_found = True
                        break

                if not is_found:
                    print(f"disobeys on line {line_number}: {cur_value}")

                preamble.append(cur_value)
                cur_sum += cur_value - preamble[0]
                del preamble[0]

    @classmethod
    def get_valid_sums(cls, values):
        valid_sums_list = []

        for value in values:
            valid_sums_list.append([])

        i1 = 0
        for value1 in values:
            i2 = 0
            for value2 in values:
                if i2 != i1:
                    valid_sums_list[i1].append(value1+value2)
                else:
                    valid_sums_list[i1].append(None)
                i2 += 1
            i1 += 1

        return valid_sums_list

    def run2(self):
        if self.path_suffix == "example":
            sum_to_find = 127
        else:
            sum_to_find = 104054607

        list_of_sums = []
        history = []
        with open(self.path, "r") as f:
            line_number = 0
            cur_sum = 0
            for line in f:
                line = line.strip()

                cur_value = int(line)
                history.append(cur_value)
                self.update_list_of_sums(list_of_sums, cur_value)

                is_found = False
                list_index = 0
                for value in list_of_sums[:-1]:
                    if value == sum_to_find:
                        is_found = True
                        break
                    list_index += 1

                if is_found:
                    smallest = min(history[list_index:line_number])
                    largest = max(history[list_index:line_number])
                    print(f"sum found from {list_index} to {line_number}: {smallest} + {largest} = {smallest + largest}")

                line_number += 1

    @classmethod
    def update_list_of_sums(cls, list_of_sums, new_value):
        if len(list_of_sums) == 0:
            list_of_sums.append(new_value)
            return

        for index in range(len(list_of_sums)):
            list_of_sums[index] += new_value
        list_of_sums.append(new_value)
