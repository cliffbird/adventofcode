from main import BaseProcessor
import re

class D15Processor(BaseProcessor):
    def run_all(self):
        #self.base_run(path_suffix="example")
        #self.base_run(path_suffix="example2")
        #self.base_run(path_suffix="example3")
        #self.base_run(path_suffix="example4")
        self.base_run()

    def run1(self):
        with open(self.path, "r") as f:
            for line in f:
                line = line.strip()
                parts = line.split(",")
        age_dict = {}
        age_dict_prior = {}

        num_turns = 0
        last_said = None
        for part in parts:
            num_turns += 1
            say = int(part)
            age_dict[say] = num_turns

            last_said = say
            #print(f"Turn {num_turns}: {say}")

        while True:
            num_turns += 1
            if last_said not in age_dict:
                say = 0
                age_dict_prior[say] = age_dict[say]
            elif last_said not in age_dict_prior:
                say = num_turns - age_dict[last_said] - 1
                if say in age_dict:
                    age_dict_prior[say] = age_dict[say]
            else:
                say = age_dict[last_said] - age_dict_prior[last_said]
                if say in age_dict:
                    age_dict_prior[say] = age_dict[say]
            age_dict[say] = num_turns

            last_said = say
            #print(f"Turn {num_turns}: {say}")
            if num_turns == 2020:
                print(f"part1: {say}")
            elif num_turns == 30000000:
                print(f"part2: {say}")
                break

