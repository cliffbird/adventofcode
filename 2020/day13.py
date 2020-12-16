from main import BaseProcessor
import numpy as np

class D13Processor(BaseProcessor):
    def run_all(self):
        self.base_run(path_suffix="example")
        for i in range(2,7):
            self.base_run(path_suffix=f"example{i}")
        self.base_run()

    def run1(self):
        with open(self.path, "r") as f:
            line_number = 0
            bus_ids = []
            for line in f:
                line = line.strip()
                if line_number == 0:
                    my_timestamp = int(line)
                elif line_number == 1:
                    for id in line.split(","):
                        if id != "x":
                            bus_ids.append(int(id))
                else:
                    raise Exception(f"Invalid line number {line_number}")
                line_number += 1

    def run1_working(self):
        with open(self.path, "r") as f:
            line_number = 0
            bus_ids = []
            for line in f:
                line = line.strip()
                if line_number == 0:
                    my_timestamp = int(line)
                elif line_number == 1:
                    for id in line.split(","):
                        if id != "x":
                            bus_ids.append(int(id))
                else:
                    raise Exception(f"Invalid line number {line_number}")
                line_number += 1
        timestamps_dict, bus_times_dict = self.get_timestamps_dict(my_timestamp, bus_ids)
        timestamps_list = list(timestamps_dict.keys())
        timestamps_list.sort()

        timestamp = timestamps_list[0]
        found_prev = None
        found_next = None
        for i in range(1, len(timestamps_list)):
            prev = timestamp
            timestamp = timestamps_list[i]
            if found_prev:
                found_next = timestamp
                break

            if timestamp == my_timestamp:
                found_prev = prev
            elif timestamp > my_timestamp:
                found_prev = prev
                found_next = timestamp
                break

        prev_difference = my_timestamp - found_prev
        next_difference = found_next - my_timestamp
        if prev_difference < next_difference and False:
            found = found_prev
            difference = prev_difference
        else:
            found = found_next
            difference = next_difference

        bus_ids = timestamps_dict[found]
        id = bus_ids.pop()
        print(f"part1: {id} * {difference} minutes = {id * difference}")

    def run2(self):
        first_bus_id = None
        bus_ids_dict = {}
        diff_from_first_bus = 0
        with open(self.path, "r") as f:
            line_number = 0
            for line in f:
                line = line.strip()
                if line_number == 0:
                    my_timestamp = int(line)
                elif line_number == 1:
                    for id in line.split(","):
                        if id != "x":
                            if first_bus_id is None:
                                first_bus_id = int(id)
                            bus_ids_dict[int(id)] = diff_from_first_bus
                        diff_from_first_bus += 1
                else:
                    raise Exception(f"Invalid line number {line_number}")
                line_number += 1

        largest_bus_id = max(bus_ids_dict.keys())
        largest_diff_from_first_bus = bus_ids_dict[largest_bus_id]

        bus_ids_sorted = list(bus_ids_dict.keys())
        bus_ids_sorted.sort(reverse=True)
        bus_ids_sorted.remove(largest_bus_id)
        time_differences_sorted = []
        for bus_id in bus_ids_sorted:
            time_differences_sorted.append(bus_ids_dict[bus_id])

        starting_timestamp = int(my_timestamp / largest_bus_id) * largest_bus_id

        largest_factor = bus_ids_sorted[0]
        largest_factor_start = self.get_first_match(starting_timestamp, largest_bus_id, largest_factor,
                                                    time_differences_sorted[0] - largest_diff_from_first_bus)
        bus_ids_sorted.remove(bus_ids_sorted[0])
        time_differences_sorted.remove(time_differences_sorted[0])

        timestamp = largest_factor_start
        while bus_ids_sorted:
            firsts_timestamp = timestamp - largest_diff_from_first_bus
            while bus_ids_sorted:
                bus_id = bus_ids_sorted[0]
                time_difference = time_differences_sorted[0]
                if (firsts_timestamp + time_difference) % bus_id != 0:
                    break
                else:
                    largest_factor = np.lcm(largest_factor, bus_id, dtype='int64')
                    bus_ids_sorted.remove(bus_ids_sorted[0])
                    time_differences_sorted.remove(time_differences_sorted[0])

                    if not bus_ids_sorted:
                        print(f"part2: {timestamp - largest_diff_from_first_bus}")
                        break

            timestamp += largest_bus_id*largest_factor

    def get_first_match(self, starting_timestamp, largest_bus_id, bus_id, time_difference_from_largest):
        timestamp = starting_timestamp + largest_bus_id
        while True:
            if (timestamp + time_difference_from_largest) % bus_id == 0:
                return timestamp

            timestamp += largest_bus_id

    def get_timestamps_dict(self, start_time, bus_ids):
        MAX_TIMESTAMP = 24*60*365*20
        bus_times_dicts = {}
        timestamps_dict = {}

        first = True
        for id in bus_ids:
            if first:
                bus_times_dicts[id] = set()
            cur_time = int(start_time / id) * id
            while cur_time < MAX_TIMESTAMP:
                if first:
                    bus_times_dicts[id].add(cur_time)
                if cur_time not in timestamps_dict:
                    timestamps_dict[cur_time] = set()
                timestamps_dict[cur_time].add(id)
                cur_time += id

        return timestamps_dict, bus_times_dicts

