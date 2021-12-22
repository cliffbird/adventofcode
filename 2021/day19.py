from collections import Counter
from copy import copy, deepcopy
import hashlib
from main import BaseProcessor
from math import ceil, floor, sqrt
from queue import SimpleQueue
import sys
from threading import Thread, Lock


class D19Processor(BaseProcessor):

    def setup(self):
        scanners = []
        if "example" not in self.path:
            #return
            pass
        with open(self.path, "r") as f:
            for y, line in enumerate(f):
                line = line.strip()
                if not line:
                    continue
                elif "scanner" in line:
                    id = int(line.split()[2])
                    scanner = Scanner(id)
                    scanners.append(scanner)
                else:
                    x,y,z = line.split(",")
                    x = int(x)
                    y = int(y)
                    z = int(z)
                    p = Point(x,y,z)
                    scanners[-1].add_point(p)

        self.scanners = scanners

        for s in scanners:
            s.process_distances()

        for i, s1 in enumerate(scanners):
            for j, s2 in enumerate(scanners):
                if i == j:
                    continue
                matches = s1.get_matches(s2)
                if matches:
                    for num_matches, s1_common_p, s2_common_p in matches:
                        if num_matches >= 1:
                            # go through the distance dict to get the matching points
                            # create a list of points based on the assumed other-scanner position
                            s1_common_ps = []
                            s2_common_ps = []
                            for distance, p1s in s1.distance_dicts[s1_common_p].items():
                                if distance in s2.distance_dicts[s2_common_p]:
                                    # iterate through the points (possible to have more than one)
                                    assert len(p1s) == 1
                                    p2s = s2.distance_dicts[s2_common_p][distance]
                                    assert len(p2s) == 1

                                    s1_common_ps.append(p1s[0])
                                    s2_common_ps.append(p2s[0])

                            if len(s1_common_ps) >= 1:
                                orientation_1to2, orientation_2to1 = get_orientation(s1_common_ps, s2_common_ps, s1_common_p, s2_common_p)
                                if orientation_1to2 and orientation_2to1:
                                    if s1 not in s2.relative_orientation:
                                        s2.relative_orientation[s1] = orientation_2to1
                                    else:
                                        assert s2.relative_orientation[s1] == orientation_2to1
                                    if s2 not in s1.relative_orientation:
                                        s1.relative_orientation[s2] = orientation_1to2
                                    else:
                                        assert s1.relative_orientation[s2] == orientation_1to2
                                    break

        source_scanner = scanners[0]
        has_source_scanners = set([source_scanner])
        need_source_scanners = set()
        for s in scanners:
            if s == source_scanner:
                continue

            if source_scanner in s.relative_orientation:
                orientation = s.relative_orientation[source_scanner]
                print(f"s{s.id} pos: {orientation.get_position()}")
                has_source_scanners.add(s)
            else:
                need_source_scanners.add(s)

        # remake the scanners relative to the source
        while need_source_scanners:
            need_source_scanners_copy = copy(need_source_scanners)
            need_source_scanners = set()
            work_done = False
            while need_source_scanners_copy:
                cur_scanner = need_source_scanners_copy.pop()
                found_secondary = False
                assert source_scanner not in cur_scanner.relative_orientation
                for sub_scanner in cur_scanner.relative_orientation:
                    if sub_scanner in has_source_scanners:
                        #relative_pos = cur_scanner.relative_pos[sub_scanner] * Point(-1,-1,-1)
                        orientation = deepcopy(cur_scanner.relative_orientation[sub_scanner])
                        # convert us to them
                        p = Point(0,0,0)
                        p.reorient(orientation)

                        other_orientation = sub_scanner.relative_orientation[source_scanner]
                        p.reorient(other_orientation)

                        orientation_to_store = Orientation([], p)
                        orientation_to_store.directions.extend(orientation.directions)
                        orientation_to_store.directions.extend(other_orientation.directions)

                        cur_scanner.relative_orientation[source_scanner] = orientation_to_store
                        print(f"s{cur_scanner.id}: pos: {orientation_to_store.get_position()}")
                        work_done = True
                        has_source_scanners.add(cur_scanner)
                        found_secondary = True
                        break
                if not found_secondary:
                    need_source_scanners.add(cur_scanner)
            if not work_done:
                print("ERROR: work was not done!")
                break

        beacons = set()
        for p in source_scanner.points:
            beacons.add(p)
        for scanner in scanners:
            if scanner == source_scanner:
                continue
            orientation = scanner.relative_orientation[source_scanner]
            for p in scanner.points:
                new_p = copy(p)
                new_p.reorient(orientation)
                beacons.add(new_p)
        print(f"part1: {len(beacons)}")

        beacons_list = list(beacons)
        beacons_list.sort(key=lambda x: x.x)
        distances = set()
        for i, s1 in enumerate(scanners):
            if s1 == source_scanner:
                continue
            s1_pos = s1.relative_orientation[source_scanner].get_position()
            for j, s2 in enumerate(scanners):
                if i == j:
                    continue

                if s2 == source_scanner:
                    s2_pos = Point(0,0,0)
                else:
                    s2_pos = s2.relative_orientation[source_scanner].get_position()
                distance = abs(s1_pos.x - s2_pos.x) + abs(s1_pos.y - s2_pos.y) + abs(s1_pos.z - s2_pos.z)
                distances.add(distance)
        print(f"part2: {max(distances)}")

    def run1(self):
        self.setup()

    def run2(self):
        pass


class Scanner:
    def __init__(self, id):
        self.id = id
        self.points = set()
        self.distance_dicts = {}
        # key = point, value = {key = distance, value = other_point}
        self.relative_orientation = {}

    def __repr__(self):
        return str(self.id)

    def add_point(self, point):
        self.points.add(point)

    def process_distances(self):
        for p in self.points:
            distance_dict = {}
            for op in self.points:
                distance = p.get_distance(op)
                if distance not in distance_dict:
                    distance_dict[distance] = []
                distance_dict[distance].append(op)
            self.distance_dicts[p] = distance_dict

    def get_matches(self, other_scanner):
        # Return a list of match tuples: number of matches, my point and other's point
        matches = []
        for my_p, my_distance_dict in self.distance_dicts.items():
            for other_p, other_distance_dict in other_scanner.distance_dicts.items():
                num_matches = 0
                for distance in my_distance_dict:
                    if distance in other_distance_dict:
                        num_matches += 1
                if num_matches:
                    matches.append((num_matches, my_p, other_p))
        matches.sort(key=lambda x: x[0])
        matches.reverse()
        return matches


class Point:
    def __init__(self, x,y,z):
        self.x = x
        self.y = y
        self.z = z

    def __hash__(self):
        return self.__repr__().__hash__()

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z

    def __repr__(self):
        return f"({self.x},{self.y},{self.z})"

    def get(self, char):
        return getattr(self, char)

    def set(self, char, value):
        setattr(self, char, value)

    def get_distance(self, other_point):
        return sqrt(((self.x - other_point.x)**2) + \
                    ((self.y - other_point.y)**2) + \
                    ((self.z - other_point.z)**2))

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        return Point(self.x * other.x, self.y * other.y, self.z * other.z)

    def reorient(self, orientation):
        temp = copy(self)
        for direction in orientation.directions:
            temp = change_direction(temp, direction)
        temp += orientation.p
        self.x = temp.x
        self.y = temp.y
        self.z = temp.z

    def reverse_reorient(self, orientation):
        temp = copy(self)
        for direction in orientation.directions[::-1]:
            temp = change_reverse(temp, direction)
        temp -= orientation.p
        self.x = temp.x
        self.y = temp.y
        self.z = temp.z

    def swap_xy(self):
        temp = self.x
        self.x = self.y
        self.y = temp

    def swap_xz(self):
        temp = self.x
        self.x = self.z
        self.z = temp

    def swap_yz(self):
        temp = self.y
        self.y = self.z
        self.z = temp

    def change_direction(self, orientation):
        temp = copy(self)
        for direction in orientation.directions[::-1]:
            temp = change_direction(temp, direction)
        self.x = temp.x
        self.y = temp.y
        self.z = temp.z


def get_orientation(p1s, p2s, p1_common, p2_common):
    # need to match mine to theirs
    # return the pos and orientation to convert us to them
    possible_directions = set()
    for direction in range(MAX_DIRECTIONS):
        for i in range(len(p1s)):
            v1 = p1s[i] - p1_common
            v2 = p2s[i] - p2_common

            v1_changed = change_direction(v1, direction)
            if v1_changed == v2:
                possible_directions.add(direction)

    orientations_1to2 = []
    for direction in possible_directions:
        # convert 1 to 2

        p1 = change_direction(p1s[0], direction)
        shift = p2s[0] - p1

        found_mismatch = False
        for i in range(1, len(p1s)):
            p1 = change_direction(p1s[i], direction)
            if p2s[i] != p1 + shift:
                found_mismatch = True
                break

        if not found_mismatch:
            orientation = Orientation([direction], shift)
            orientations_1to2.append(orientation)

    if len(orientations_1to2) != 1:
        return None, None

    orientations_2to1 = []
    for direction in range(MAX_DIRECTIONS):
        # convert 2 to 1
        p2 = change_direction(p2s[0], direction)
        shift = p1s[0] - p2
        found_mismatch = False
        for i in range(1, len(p2s)):
            p2 = change_direction(p2s[i], direction)
            if p1s[i] != p2 + shift:
                found_mismatch = True
                break

        if not found_mismatch:
            orientation = Orientation([direction], shift)
            orientations_2to1.append(orientation)

    assert len(orientations_1to2) == 1 and len(orientations_2to1) == 1

    # Test orientation
    for i in range(len(p1s)):
        p1 = copy(p1s[i])
        p1.reorient(orientations_1to2[0])
        assert p1 == p2s[i]

        p2 = copy(p2s[i])
        p2.reorient(orientations_2to1[0])
        assert p2 == p1s[i]

    return orientations_1to2[0], orientations_2to1[0]


class Orientation:
    def __init__(self, directions, p):
        self.directions = directions
        self.p = copy(p)

    def __repr__(self):
        return f"{self.p} - {','.join([str(x) for x in self.directions])}"

    def __hash__(self):
        return self.__repr__().__hash__()

    def __eq__(self, other):
        is_equal = True
        if self.p == other.p and len(self.directions) == len(other.directions):
            for i, direction in enumerate(self.directions):
                if direction != other.directions[i]:
                    is_equal = False
                    break
        return is_equal

    def get_position(self):
        return copy(self.p)
        position = copy(self.p)
        for direction in self.directions:
            position = change_direction(position, direction)
        position *= Point(-1, -1, -1)
        return position

MAX_DIRECTIONS = 24

def change_direction(p, direction):
    # first value is straight-back, second value is right-left, third value is up-down
    p2 = copy(p)
    if direction == 0:
        # facing straight
        pass
    elif direction == 1:
        # facing left (-y)
        p2.y *= -1
        p2.swap_xy()
    elif direction == 2:
        # facing back (-x, -y)
        p2.x *= -1
        p2.y *= -1
    elif direction == 3:
        # facing right (y, -x)
        p2.x *= -1
        p2.swap_xy()

    elif direction == 4:
        # facing up
        p2.x *= -1
        p2.swap_xz()
    elif direction == 5:
        # face left then up
        p2.swap_xz()
        p2.swap_yz()
    elif direction == 6:
        # face back then up
        p2.y *= -1
        p2.swap_xz()
    elif direction == 7:
        # face right then up
        p2.x *= -1
        p2.y *= -1
        p2.swap_xz()
        p2.swap_yz()

    elif direction == 8:
        # facing down
        p2.z *= -1
        p2.swap_xz()
    elif direction == 9:
        # face left then down
        p2.z *= -1
        p2.y *= -1
        p2.swap_xz()
        p2.swap_yz()
    elif direction == 10:
        # face back then down
        p2.z *= -1
        p2.x *= -1
        p2.y *= -1
        p2.swap_xz()
    elif direction == 11:
        #face right then down
        p2.z *= -1
        p2.x *= -1
        p2.swap_xz()
        p2.swap_yz()

    elif direction == 12:
        # face straight, roll left
        p2.y *= -1
        p2.swap_yz()
    elif direction == 13:
        # face left, roll left
        p2.y *= -1
        p2.x *= -1
        p2.swap_xy()
        p2.swap_yz()
    elif direction == 14:
        # face back, roll left
        p2.x *= -1
        p2.swap_yz()
    elif direction == 15:
        # face right, roll left
        p2.swap_xy()
        p2.swap_yz()

    elif direction == 16:
        # face straight, roll right
        p2.z *= -1
        p2.swap_yz()
    elif direction == 17:
        # face left, roll right
        p2.y *= -1
        p2.swap_xy()
        p2.z *= -1
        p2.swap_yz()
    elif direction == 18:
        # face back, roll right
        p2.x *= -1
        p2.y *= -1
        p2.z *= -1
        p2.swap_yz()
    elif direction == 19:
        # face right, roll right
        p2.x *= -1
        p2.z *= -1
        p2.swap_xy()
        p2.swap_yz()

    elif direction == 20:
        # face straight, upside-down
        p2.y *= -1
        p2.z *= -1
    elif direction == 21:
        # face left, upside-down
        p2.y *= -1
        p2.x *= -1
        p2.z *= -1
        p2.swap_xy()
    elif direction == 22:
        # face back, upside-down
        p2.x *= -1
        p2.z *= -1
    elif direction == 23:
        # face right, upside-down
        p2.swap_xy()
        p2.x *= -1
        p2.z *= -1
    return p2

def change_reverse(p, direction):
    # first value is straight-back, second value is right-left, third value is up-down
    new_direction = None
    if direction == 0:
        # facing straight
        new_direction = 0
    elif direction == 1:
        # facing left (-y)
        new_direction = 3
    elif direction == 2:
        # facing back (-x, -y)
        new_direction = 2
    elif direction == 3:
        # facing right (y, -x)
        new_direction = 1

    elif direction == 4:
        # facing up
        new_direction = 8
    elif direction == 5:
        # face left then up
        new_direction = 15
    elif direction == 6:
        # face back then up
        new_direction = 6
    elif direction == 7:
        # face right then up
        new_direction = 17

    elif direction == 8:
        # facing down
        new_direction = 4
    elif direction == 9:
        # face left then down
        new_direction = 19
    elif direction == 10:
        # face back then down
        new_direction = 10
    elif direction == 11:
        # face right then down
        new_direction = 13

    elif direction == 12:
        # face straight, roll left
        new_direction = 16
    elif direction == 13:
        # face left, roll left
        new_direction = 11
    elif direction == 14:
        # face back, roll left
        new_direction = 14
    elif direction == 15:
        # face right, roll left
        new_direction = 5

    elif direction == 16:
        # face straight, roll right
        new_direction = 12
    elif direction == 17:
        # face left, roll right
        new_direction = 7
    elif direction == 18:
        # face back, roll right
        new_direction = 18
    elif direction == 19:
        # face right, roll right
        new_direction = 9

    elif direction == 20:
        # face straight, upside-down
        new_direction = 20
    elif direction == 21:
        # face left, upside-down
        new_direction = 21
    elif direction == 22:
        # face back, upside-down
        new_direction = 22
    elif direction == 23:
        # face right, upside-down
        new_direction = 24
    return change_direction(p, new_direction)
