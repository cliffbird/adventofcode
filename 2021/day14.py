from collections import Counter
from copy import copy, deepcopy
from main import BaseProcessor
from queue import SimpleQueue
from threading import Thread, Lock


class D14Processor(BaseProcessor):

    def setup(self):
        stage = 0
        p = Process()
        with open(self.path, "r") as f:
            for i, line in enumerate(f):
                line = line.strip()

                if not line:
                    stage += 1
                    continue

                if stage == 0:
                    p.do_template(line)

                elif stage == 1:
                    rule = line
                    pair_match, element_to_insert = rule.split(" -> ")
                    p.insert_rule(pair_match, element_to_insert)

        print(f"Template:     {p.template}")
        p.do_level_rules()

        result = p.do_rules(1)
        result = p.do_rules(2)

        i = 10
        result = p.do_rules(i)
        #print(f"After step {i}: {len(result)}: {p.most_minus_least(result)}")
        print(f"After step {i}: {result}")

        i = 40
        result = p.do_rules(i)
        #print(f"After step {i}: {len(result)}: {p.most_minus_least(result)}")
        print(f"After step {i}: {result}")

        print(f"part2: {0}")


    def run1(self):
        self.setup()

    def run2(self):
        pass

class Process:
    def __init__(self):
        #self.pairs = Pairs()
        self.template = None
        self.rules = {}

    def do_template(self, template):
        self.template = template
        self.pairs = []

        prev_char = template[1]
        for i, char in enumerate(template[1:]):
            self.pairs.append(prev_char + char)
            prev_char = char

    def insert_rule(self, pair_match, element_to_insert):
        self.rules[pair_match] = element_to_insert

    def do_level_rules(self):
        self.level_rules = Rules(self.rules)

    def do_rules(self, max_depth):
        count_dict = {}
        for pair, rchar in self.rules.items():
            for char in [pair[0], pair[1], rchar]:
                count_dict[char] = 0
        prev_char = self.template[0]
        count_dict[prev_char] += 1
        for char in self.template[1:]:
            count_dict[char] += 1
            pair = prev_char + char
            prev_char = char
            rule = self.level_rules.rules[pair]
            cur_row = set([rule])
            count_dict[rule.rc] += 1
            multiplier = {}
            rule_count = {}
            next_rule_count = {}
            for pair, rule in self.level_rules.rules.items():
                multiplier[rule] = 1
                rule_count[rule] = 1
                next_rule_count[rule] = 0

            for i in range(max_depth-1):
                new_row = set()
                for rule in cur_row:
                    count_dict[rule.rp1.rc] += rule_count[rule]
                    next_rule_count[rule.rp1] += rule_count[rule]
                    new_row.add(rule.rp1)
                    count_dict[rule.rp2.rc] += rule_count[rule]
                    next_rule_count[rule.rp2] += rule_count[rule]
                    new_row.add(rule.rp2)
                rule_count = next_rule_count
                next_rule_count = {}
                for pair, rule in self.level_rules.rules.items():
                    next_rule_count[rule] = 0
                cur_row = new_row

        return self.most_minus_least(count_dict)

    def most_minus_least(self, count_dict):
        count_list = []
        for char, count in count_dict.items():
            count_list.append((char, count))
        count_list_sorted = sorted(count_list, key=lambda x: x[1])
        value = count_list_sorted[-1][1] - count_list_sorted[0][1]
        return value

class Rules:
    def __init__(self, rule_pairs):
        self.rules = {}
        for pair, char in rule_pairs.items():
            self.rules[pair] = Rule(pair, char)

        for pair, rule in self.rules.items():
            rp1_str = rule.pair[0] + rule.rc
            rule.rp1 = self.rules[rp1_str]

            rp2_str = rule.rc + rule.pair[1]
            rule.rp2 = self.rules[rp2_str]


class Rule:
    def __init__(self, pair_str, result_char):
        self.pair = pair_str
        self.rc = result_char
        self.rp1 = None
        self.rp2 = None
