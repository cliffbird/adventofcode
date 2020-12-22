from main import BaseProcessor

class D19Processor(BaseProcessor):
    def run_all(self):
        self.base_run(path_suffix="example")
        self.base_run(path_suffix="example2")
        self.base_run(path_suffix="example3")
        self.base_run(path_suffix="example4")
        self.base_run()

    def run1(self):
        self.rules = {}
        messages = []
        with open(self.path, "r") as f:
            section = "rules"
            for line in f:
                line = line.strip()
                if not line:
                    section = "messages"
                if section == "rules":
                    rule_number, rest = line.split(": ")
                    parts = rest.split()

                    self.rules[rule_number] = {}
                    if "|" in parts:
                        or_index = parts.index("|")
                        self.rules[rule_number]["list"] = parts[:or_index]
                        self.rules[rule_number]["or"] = parts[or_index+1:]
                    else:
                        self.rules[rule_number]["list"] = parts

                elif section == "messages":
                    messages.append(line)

        if self.path_suffix == "example" or self.path_suffix == "example2":
            self.max_message_length = None
        else:
            self.max_message_length = 0
            for message in messages:
                if len(message) > self.max_message_length:
                    self.max_message_length = len(message)

        self.answers = {}
        rule_0_matches = self.get_rule_matches("0")

        matches = set()
        for message in messages:
            if message in rule_0_matches:
                matches.add(message)

        if self.path_suffix == "example" or self.path_suffix == "example2":
            print(f"part1: {rule_0_matches}")
        else:
            print(f"part1: {len(matches)}")

    def get_rule_matches(self, rule_number):
        if rule_number in self.answers:
            return self.answers[rule_number]
        ultimate_answer_set = set()

        for list_or, parts in self.rules[rule_number].items():
            answer_set = set()
            for sub in parts:
                if '"' in sub:
                    # is a direct answer
                    answer = sub.strip('"')
                    if answer_set:
                        new_answer_set = set()
                        for old_answer in answer_set:
                            new_answer_set.add(old_answer + answer)
                        answer_set = new_answer_set
                    else:
                        answer_set.add(answer)
                else:
                    # is a sub rule
                    sub_answer_set = self.get_rule_matches(sub)
                    if answer_set:
                        new_answer_set = set()
                        for old_answer in answer_set:
                            for sub_answer in sub_answer_set:
                                new_answer_set.add(old_answer + sub_answer)
                        answer_set = new_answer_set
                    else:
                        answer_set = sub_answer_set
            ultimate_answer_set = ultimate_answer_set.union(answer_set)
        self.answers[rule_number] = ultimate_answer_set
        return ultimate_answer_set

    def run2(self):
        if self.path_suffix == "example" or self.path_suffix == "example2" or self.path_suffix == "example3":
            return

        self.rules = {}
        messages = []
        with open(self.path, "r") as f:
            section = "rules"
            for line in f:
                line = line.strip()
                if not line:
                    section = "messages"
                if section == "rules":
                    rule_number, rest = line.split(": ")
                    if rule_number == "8":
                        rule_number, rest = "8: 42 | 42 8".split(": ")
                    elif rule_number == "11":
                        rule_number, rest = "11: 42 31 | 42 11 31".split(": ")
                    parts = rest.split()

                    self.rules[rule_number] = {}
                    if "|" in parts:
                        or_index = parts.index("|")
                        self.rules[rule_number]["list"] = parts[:or_index]
                        self.rules[rule_number]["or"] = parts[or_index + 1:]
                    else:
                        self.rules[rule_number]["list"] = parts

                elif section == "messages":
                    messages.append(line)

        self.max_message_length = 0
        for message in messages:
            if len(message) > self.max_message_length:
                self.max_message_length = len(message)

        self.answers = {}

        if "42" in self.rules:
            rule_42_matches = self.get_rule_matches("42")
        if "31" in self.rules:
            rule_31_matches = self.get_rule_matches("31")

        rule_42_match_length = None
        for rule_42_match in rule_42_matches:
            if not rule_42_match_length:
                rule_42_match_length = len(rule_42_match)
            assert rule_42_match_length == len(rule_42_match)

        rule_31_match_length = None
        for rule_31_match in rule_31_matches:
            if not rule_31_match_length:
                rule_31_match_length = len(rule_31_match)
            assert rule_31_match_length == len(rule_31_match)

        matches = set()
        for message in messages:
            cur_message = message
            num_42s = 0
            while cur_message[:rule_42_match_length] in rule_42_matches:
                cur_message = cur_message[rule_42_match_length:]
                num_42s += 1

            num_31s = 0
            while cur_message[:rule_31_match_length] in rule_31_matches and num_31s < num_42s - 1:
                cur_message = cur_message[rule_31_match_length:]
                num_31s += 1
                if cur_message == "":
                    matches.add(message)

        print(f"part2: {len(matches)}")
