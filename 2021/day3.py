from copy import copy
from main import BaseProcessor

class D3Processor(BaseProcessor):

    def run1(self):
        with open(self.path, "r") as f:
            num_bits = None
            counts = []
            total = 0
            for line in f.readlines():
                line = line.strip()
                if num_bits is None:
                    num_bits = len(line)
                    for i in range(num_bits):
                        counts.append(0)
                for i in range(num_bits):
                    if line[i] != "0":
                        counts[i] += 1
                total += 1

            gamma = 0
            epsilon = 0
            for count in counts:
                num_0s = total - count
                num_1s = count
                gamma *= 2
                epsilon *= 2
                if num_1s > num_0s:
                    gamma += 1
                else:
                    epsilon += 1

        print(f"part1: {gamma*epsilon}")

    def run2(self):
        with open(self.path, "r") as f:
            num_bits = None
            counts = []
            total = 0
            values = []
            for line in f.readlines():
                line = line.strip()
                if num_bits is None:
                    num_bits = len(line)
                    for i in range(num_bits):
                        counts.append(0)
                for i in range(num_bits):
                    if line[i] != "0":
                        counts[i] += 1
                values.append(line)
                total += 1

            most_common = 0
            least_common = 0
            for count in counts:
                num_0s = total - count
                num_1s = count
                most_common *= 2
                least_common *= 2
                if num_1s >= num_0s:
                    most_common += 1
                else:
                    least_common += 1

            o2_rating = None
            o2_values = copy(values)
            for i in range(num_bits):
                list_0s = []
                list_1s = []

                for j in range(len(o2_values)):
                    if o2_values[j][i] == "0":
                        list_0s.append(o2_values[j])
                    else:
                        list_1s.append(o2_values[j])

                if len(list_1s) >= len(list_0s):
                    o2_values = copy(list_1s)
                else:
                    o2_values = copy(list_0s)

                if len(o2_values) == 1:
                    o2_rating = o2_values.pop()
                    break

            temp = 0
            for value in o2_rating:
                temp *= 2
                if value == "1":
                    temp += 1
            o2_rating = temp

            co2_rating = None
            co2_values = copy(values)
            for i in range(num_bits):
                list_0s = []
                list_1s = []

                for j in range(len(co2_values)):
                    if co2_values[j][i] == "0":
                        list_0s.append(co2_values[j])
                    else:
                        list_1s.append(co2_values[j])

                if len(list_1s) >= len(list_0s):
                    co2_values = copy(list_0s)
                else:
                    co2_values = copy(list_1s)

                if len(co2_values) == 1:
                    co2_rating = co2_values.pop()
                    break

            temp = 0
            for value in co2_rating:
                temp *= 2
                if value == "1":
                    temp += 1
            co2_rating = temp

        print(f"part2: {o2_rating*co2_rating}")