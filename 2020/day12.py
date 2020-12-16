from main import BaseProcessor

class D12Processor(BaseProcessor):
    def run1(self):
        self.cur_pos = (0, 0)
        self.dir = "E"
        with open(self.path, "r") as f:
            for line in f:
                line = line.strip()
                self.do_action_part1(line)

        print(f"part1: |{self.cur_pos[0]}| + |{self.cur_pos[1]}| = {abs(self.cur_pos[0]) + abs(self.cur_pos[1])}")

    def do_action_part1(self, action_str):
        action = action_str[0]
        value = int(action_str[1:])
        if action == "N":
            self.cur_pos = (self.cur_pos[0], self.cur_pos[1] + value)
        elif action == "S":
            self.cur_pos = (self.cur_pos[0], self.cur_pos[1] - value)
        elif action == "E":
            self.cur_pos = (self.cur_pos[0] + value, self.cur_pos[1])
        elif action == "W":
            self.cur_pos = (self.cur_pos[0] - value, self.cur_pos[1])
        elif action == "L" or action == "R":
            self.rotate_ship(action, value)
        elif action == "F":
            if self.dir == "N":
                self.cur_pos = (self.cur_pos[0], self.cur_pos[1] + value)
            elif self.dir == "S":
                self.cur_pos = (self.cur_pos[0], self.cur_pos[1] - value)
            elif self.dir == "E":
                self.cur_pos = (self.cur_pos[0] + value, self.cur_pos[1])
            elif self.dir == "W":
                self.cur_pos = (self.cur_pos[0] - value, self.cur_pos[1])

    def rotate_ship(self, dir, degrees):
        cur_degree = 0
        if self.dir == "N":
            cur_degree = 90
        elif self.dir == "S":
            cur_degree = 270
        elif self.dir == "E":
            cur_degree = 0
        elif self.dir == "W":
            cur_degree = 180

        if dir == "L":
            cur_degree += degrees
        elif dir == "R":
            cur_degree -= degrees

        if cur_degree < 0:
            cur_degree %= -360
            cur_degree += 360
            assert cur_degree > 0

        cur_degree %= 360
        if cur_degree == 90:
            self.dir = "N"
        elif cur_degree == 180:
            self.dir = "W"
        elif cur_degree == 270:
            self.dir = "S"
        elif cur_degree == 0:
            self.dir = "E"

    def run2(self):
        self.cur_pos = (0, 0)
        self.waypoint = (10, 1)
        with open(self.path, "r") as f:
            for line in f:
                line = line.strip()
                self.do_action_part2(line)

        print(f"part2: |{self.cur_pos[0]}| + |{self.cur_pos[1]}| = {abs(self.cur_pos[0]) + abs(self.cur_pos[1])}")

    def do_action_part2(self, action_str):
        action = action_str[0]
        value = int(action_str[1:])
        if action == "N":
            self.waypoint = (self.waypoint[0], self.waypoint[1] + value)
        elif action == "S":
            self.waypoint = (self.waypoint[0], self.waypoint[1] - value)
        elif action == "E":
            self.waypoint = (self.waypoint[0] + value, self.waypoint[1])
        elif action == "W":
            self.waypoint = (self.waypoint[0] - value, self.waypoint[1])
        elif action == "L" or action == "R":
            self.rotate_waypoint(action, value)
        elif action == "F":
            self.cur_pos = (self.cur_pos[0] + self.waypoint[0]*value, self.cur_pos[1] + self.waypoint[1]*value)

    def rotate_waypoint(self, dir, degrees):
        cur_degree = 0

        if dir == "L":
            cur_degree += degrees
        elif dir == "R":
            cur_degree -= degrees

        if cur_degree < 0:
            cur_degree %= -360
            cur_degree += 360
            assert cur_degree > 0

        cur_degree %= 360
        if cur_degree == 90:
            new_waypoint = (-self.waypoint[1], self.waypoint[0])
        elif cur_degree == 180:
            new_waypoint = (-self.waypoint[0], -self.waypoint[1])
        elif cur_degree == 270:
            new_waypoint = (self.waypoint[1], -self.waypoint[0])
        elif cur_degree == 0:
            new_waypoint = self.waypoint
        self.waypoint = new_waypoint
