from main import BaseProcessor


class D7Processor(BaseProcessor):
    MAIN_BAGS = ["mirrored silver"]

    def parse(self):
        outer_bag_colors_with_gold = set()
        contain_map = {}
        with open(self.path, "r") as f:
            for line in f:
                line = line.strip()
                parts = line.split(" contain ")
                left = parts[0]
                right = parts[1]

                l_parts = left.split()
                l_adj = l_parts[0]
                l_color = l_parts[1]

                contain_map[f"{l_adj} {l_color}"] = set()

                r_parts = right.split(",")
                for r_part in r_parts:
                    if "no other bags" in r_part:
                        continue
                    inner_parts = r_part.split()
                    r_num = inner_parts[0]
                    r_adj = inner_parts[1]
                    r_color = inner_parts[2]

                    contain_map[f"{l_adj} {l_color}"].add(f"{r_adj} {r_color}")
                    if r_adj == "shiny" and r_color == "gold":
                        outer_bag_colors_with_gold.add(f"{l_adj} {l_color}")
        while True:
            added_sub_bag = False
            for outer_bag, outer_bag_set in contain_map.items():
                if outer_bag in outer_bag_colors_with_gold:
                    continue
                for color_find in set(outer_bag_colors_with_gold):
                    if color_find in outer_bag_set:
                        outer_bag_colors_with_gold.add(outer_bag)
                        added_sub_bag = True
            if not added_sub_bag:
                break
        return len(outer_bag_colors_with_gold)

    def run1(self):
        count = self.parse()
        print(f"part1: {count}")

    def run2(self):
        outer_bag_colors_with_gold = set()
        contain_map = {}
        with open(self.path, "r") as f:
            for line in f:
                line = line.strip()
                parts = line.split(" contain ")
                left = parts[0]
                right = parts[1]

                l_parts = left.split()
                l_color = f"{l_parts[0]} {l_parts[1]}"

                contain_map[l_color] = []

                r_parts = right.split(",")
                for r_part in r_parts:
                    if "no other bags" in r_part:
                        continue
                    inner_parts = r_part.split()
                    r_num = int(inner_parts[0])
                    r_color = f"{inner_parts[1]} {inner_parts[2]}"

                    contain_map[l_color].append((r_num, r_color))

        self.contain_map = contain_map
        count = self.get_bag_count("shiny gold")
        print(f"part2: {count}")

    def get_bag_count(self, color):
        total = 0
        list_to_check = self.contain_map[color]
        for item in list_to_check:
            i_count = item[0]
            i_color = item[1]

            total += i_count + i_count * self.get_bag_count(i_color)

        return total