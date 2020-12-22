import json
from main import BaseProcessor

class D16Processor(BaseProcessor):
    def run_all(self):
        self.base_run(path_suffix="example")
        self.base_run(path_suffix="example2")
        #self.base_run(path_suffix="example3")
        #self.base_run(path_suffix="example4")
        self.base_run()

    def run1(self):
        self.valid_tickets = []
        invalid_values = []

        section = "info"
        valid_interval_set = IntervalSet()
        with open(self.path, "r") as f:
            for line in f:
                line = line.strip()

                if not line:
                    continue
                elif line == "your ticket:":
                    section = "your ticket"
                    continue
                elif line == "nearby tickets:":
                    section = "nearby tickets"
                    continue

                if section == "info":
                    parts = line.split(":")
                    parts = parts[1].split()
                    for part in parts:
                        if "-" in part:
                            interval_numbers = part.split("-")
                            start = int(interval_numbers[0])
                            end = int(interval_numbers[1])
                            valid_interval_set.add_range(start, end)
                elif section == "your ticket" or section == "nearby tickets":
                    if section == "your ticket":
                        self.my_ticket = line
                    numbers = line.split(",")
                    is_valid = True
                    for number in numbers:
                        number = int(number)
                        if not valid_interval_set.is_valid(number):
                            invalid_values.append(number)
                            is_valid = False
                    if is_valid:
                        self.valid_tickets.append(line)

        invalid_sum = 0
        invalid_values_str = []
        for invalid_value in invalid_values:
            invalid_sum += invalid_value
            invalid_values_str.append(f"{invalid_value}")
        print(f"part1: {' + '.join(invalid_values_str)} = {invalid_sum}")


    def run2(self):
        field_dict = {}

        with open(self.path, "r") as f:
            for line in f:
                line = line.strip()

                if not line:
                    break
                elif line == "your ticket:":
                    break
                elif line == "nearby tickets:":
                    break

                parts = line.split(":")
                field_name = parts[0]
                parts = parts[1].split()
                field_dict[field_name] = IntervalSet()
                for part in parts:
                    if "-" in part:
                        interval_numbers = part.split("-")
                        start = int(interval_numbers[0])
                        end = int(interval_numbers[1])
                        field_dict[field_name].add_range(start, end)

        # build field values
        field_values_table = []
        for value in self.valid_tickets[0].split(","):
            field_values_table.append([])

        for ticket in self.valid_tickets:
            parts = ticket.split(",")
            for column in range(len(parts)):
                value = int(parts[column])
                field_values_table[column].append(value)

        field_names = set(field_dict.keys())

        # build a table of likely fields for each column
        column_to_valid_field_names = []
        for column in range(len(field_values_table)):
            column_to_valid_field_names.append(set())

        for column in range(len(field_values_table)):
            field_values = field_values_table[column]

            for field_name, field_interval_set in field_dict.items():
                invalid_found = False
                for value in field_values:
                    if not field_interval_set.is_valid(value):
                        invalid_found = True
                        break

                if not invalid_found:
                    column_to_valid_field_names[column].add(field_name)


        num_len_1 = 0
        found_field_names = set()
        while num_len_1 != len(column_to_valid_field_names):
            found_field_name = None
            for column in range(len(column_to_valid_field_names)):
                valid_field_names = column_to_valid_field_names[column]
                if len(valid_field_names) == 1:
                    field_name = valid_field_names.pop()
                    valid_field_names.add(field_name)
                    if field_name in found_field_names:
                        continue
                    found_field_names.add(field_name)
                    found_field_name = field_name
                    num_len_1 += 1
                    break

            if found_field_name:
                # loop through  and remove the field name from others
                for column in range(len(column_to_valid_field_names)):
                    valid_field_names = column_to_valid_field_names[column]
                    if len(valid_field_names) != 1 and found_field_name in valid_field_names:
                        valid_field_names.remove(found_field_name)

        if self.path_suffix == "example2":
            print(f"part2: {column_to_valid_field_names}")

        my_ticket_numbers = self.my_ticket.split(",")
        strings = []
        values = []
        for column in range(len(column_to_valid_field_names)):
            valid_field_names = column_to_valid_field_names[column]
            valid_field_name = valid_field_names.pop()
            if valid_field_name.startswith("departure"):
                strings.append(my_ticket_numbers[column])
                values.append(int(my_ticket_numbers[column]))

        if self.path_suffix == "":
            product = 1
            for value in values:
                product *= value

            print(f"part2: {' * '.join(strings)} = {product}")





class IntervalSet:
    def __init__(self):
        self.ranges = []

    def add_range(self, start, end):
        for range in self.ranges:
            if range.is_within(start):
                range.extend_end(end)
                return
            elif range.is_within(end):
                range.extend_start(start)
                return

        # not yet added
        index = 0
        for range in self.ranges:
            if end < range.start:
                break
            index += 1
        self.ranges.insert(index, Range(start, end))

    def is_valid(self, value):
        for range in self.ranges:
            if range.is_within(value):
                return True
        return False

class Range:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def extend_start(self, new_start):
        self.start = new_start

    def extend_end(self, new_end):
        self.end = new_end

    def is_within(self, value):
        return value >= self.start and value <= self.end
