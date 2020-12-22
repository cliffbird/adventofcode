from copy import deepcopy
from main import BaseProcessor
from math import sqrt
import re

class D20Processor(BaseProcessor):
    def run_all(self):
        self.base_run(path_suffix="example")
        self.base_run()

    def run1(self):
        self.all_tiles_dict = {}
        self.all_tile_names_set = set()
        with open(self.path, "r") as f:
            section = "title"
            tile_name = None
            for line in f:
                line = line.strip()

                if not line:
                    section = "title"
                    continue

                if section == "title":
                    parts = re.split(" |:", line)
                    tile_name = parts[1]
                    self.all_tiles_dict[tile_name] = Tile(tile_name)
                    self.all_tile_names_set.add(tile_name)
                    section = "data"
                else:
                    self.all_tiles_dict[tile_name].add_row(line)

        num_tiles = len(self.all_tile_names_set)
        self.image_width = int(sqrt(num_tiles))

        self.corner_tiles = {} # key is the tile, value is another dict where key is the side and value is the neighbor tile on that side

        while len(self.corner_tiles) < 4:
            tile1_name = self.all_tile_names_set.pop()
            tile1 = self.all_tiles_dict[tile1_name]

            while tile1 in self.corner_tiles:
                self.all_tile_names_set.add(tile1_name)
                tile1_name = self.all_tile_names_set.pop()
                tile1 = self.all_tiles_dict[tile1_name]

            match_side_dict = self.get_all_matches(tile1_name)

            num_sides = 0
            neighbors = {}
            sides = set()
            for side, tile_names in match_side_dict.items():
                if tile_names:
                    num_sides += 1
                    sides.add(side)
                for tile_name in tile_names:
                    neighbors[self.all_tiles_dict[tile_name]] = side
            if num_sides == 2:
                self.corner_tiles[tile1] = {}
                for neighbor_tile, side in neighbors.items():
                    self.corner_tiles[tile1][side] = neighbor_tile

            self.all_tile_names_set.add(tile1.tile_name)

        product = 1
        for corner_tile in self.corner_tiles:
            product *= int(corner_tile.tile_name)
        print(f"part1: {' * '.join([x.tile_name for x in self.corner_tiles])} = {product}")

    def get_all_matches(self, tile_name1):
        match_side_dict = {TOP: set(), RIGHT: set(), BOTTOM: set(), LEFT: set()}
        remaining_tile_names = deepcopy(self.all_tile_names_set)
        if tile_name1 in remaining_tile_names:
            remaining_tile_names.remove(tile_name1)
        for tile_name2 in remaining_tile_names:
            tile1 = self.all_tiles_dict[tile_name1]
            tile2 = self.all_tiles_dict[tile_name2]
            matching_dict = tile1.get_matching_dict(tile2)
            for side in matching_dict:
                match_side_dict[side].add(tile_name2)
        return match_side_dict


    def run2(self):
        # build image, start with one corner
        border_around = []

        first_corner = None

        while first_corner is None:
            for corner_tile, directions_to_neighbors in self.corner_tiles.items():
                directions_to_neighbors = list(directions_to_neighbors.keys())
                if (directions_to_neighbors[0] == RIGHT and directions_to_neighbors[1] == BOTTOM) or \
                   (directions_to_neighbors[0] == BOTTOM and directions_to_neighbors[1] == RIGHT):
                    first_corner = corner_tile
                    break

            if first_corner:
                break

            # rotate all the corner tiles, re-obtain neighbors, and try again
            for corner_tile, directions_to_neighbors in self.corner_tiles.items():
                corner_tile.rotate_clockwise()

                for dummy_side, neighbor_tile in directions_to_neighbors.items():
                    self.corner_tiles[corner_tile] = {} # clear old values
                    match_side_dict = self.get_all_matches(corner_tile.tile_name)
                    for side, tile_names in match_side_dict.items():
                        if tile_names:
                            self.corner_tiles[corner_tile][side] = neighbor_tile

        # build borders
        border_around.append(first_corner)

        cur_tile_name = first_corner.tile_name
        cur_direction = RIGHT

        remaining_tile_names = deepcopy(self.all_tile_names_set)
        remaining_tile_names.remove(cur_tile_name)
        while len(border_around) < 2 * self.image_width + 2*(self.image_width - 2):
            next_possible_dict = {} # key is tile_name, value is orientation count
            cur_tile = self.all_tiles_dict[cur_tile_name]
            for next_tile_name in remaining_tile_names:
                next_tile = self.all_tiles_dict[next_tile_name]
                matching_dict = cur_tile.get_matching_dict(next_tile)
                if cur_direction in matching_dict:
                    next_possible_dict[next_tile_name] = matching_dict[cur_direction]

            if len(next_possible_dict) == 1:
                for cur_tile_name, orientation_count in next_possible_dict.items():
                    prev_tile = cur_tile
                    cur_tile = self.all_tiles_dict[cur_tile_name]
                    cur_tile.apply_orientation_count(orientation_count)
                    assert prev_tile.borders[cur_direction] == cur_tile.borders[(cur_direction+2)%4]
                    border_around.append(cur_tile)
                    remaining_tile_names.remove(cur_tile_name)
                    break
            else:
                raise Exception(f"Hard: {len(next_possible_dict)}")

            if cur_tile in self.corner_tiles:
                cur_direction += 1
                cur_direction %= 4

        # build rows
        rows = []
        for i in range(self.image_width):
            rows.append([])
        # Build the first row (edge)
        for i in range(self.image_width):
            rows[0].append(border_around[i])

        # Build the remaining rows
        cur_direction = RIGHT
        for row_number in range(1, self.image_width - 1):
            cur_row = rows[row_number]
            cur_tile = border_around[-row_number]
            cur_tile_name = cur_tile.tile_name
            cur_row.append(cur_tile)

            while len(cur_row) < self.image_width - 1:
                next_possible_dict = {}  # key is tile_name, value is orientation count
                cur_tile = self.all_tiles_dict[cur_tile_name]
                for next_tile_name in remaining_tile_names:
                    next_tile = self.all_tiles_dict[next_tile_name]
                    matching_dict = cur_tile.get_matching_dict(next_tile)
                    if cur_direction in matching_dict:
                        next_possible_dict[next_tile_name] = matching_dict[cur_direction]

                if len(next_possible_dict) == 1:
                    for cur_tile_name, orientation_count in next_possible_dict.items():
                        cur_tile = self.all_tiles_dict[cur_tile_name]
                        cur_tile.apply_orientation_count(orientation_count)
                        cur_row.append(cur_tile)
                        remaining_tile_names.remove(cur_tile_name)
                        break
                else:
                    raise Exception(f"Hard: {len(next_possible_dict)}")

            cur_row.append(border_around[self.image_width + row_number - 1])

        # Build the last row (edge)
        for i in range(self.image_width):
            rows[self.image_width - 1].append(border_around[-self.image_width-i+1])

        # Print image
        output_rows = []
        for row_index in range(len(rows)):
            row = rows[row_index]
            for tile_index in range(len(row)):
                tile = row[tile_index]
                data_no_borders = tile.get_no_borders()
                for tile_row_index in range(len(data_no_borders)):
                    tile_row = data_no_borders[tile_row_index]
                    if tile_index == 0:
                        output_rows.append(tile_row)
                    else:
                        output_rows[row_index * len(data_no_borders) + tile_row_index] += tile_row

        image_tile = Tile("image")
        for output_row in output_rows:
            image_tile.add_row(output_row)

        monster_positions_dict = {} # key is orientation_count, value is a set of monster positions (row, col)

        for i in range(8):
            monster_positions_set = image_tile.find_monster()
            if monster_positions_set:
                monster_positions_dict[i] = monster_positions_set

            image_tile.rotate_clockwise()
            if i == 3 or i == 7:
                image_tile.flip()

        for i in range(8):
            if i in monster_positions_dict:
                monster_positions_set = monster_positions_dict[i]
                for monster_position in monster_positions_set:
                    image_tile.add_monster(monster_position)

            image_tile.rotate_clockwise()
            if i == 3 or i == 7:
                image_tile.flip()

        for row in image_tile.rows:
            print(row)

        print(f"part2: {image_tile.get_water_rougness()}")


TOP = 0
RIGHT = 1
BOTTOM = 2
LEFT = 3

class Tile:
    def __init__(self, tile_name):
        self.tile_name = tile_name
        self.rows = []
        self.borders = None
        self.width = 0

    def add_row(self, line):
        self.rows.append(line)
        self.width += 1

    def get_borders(self):
        if self.borders:
            return self.borders

        # top, right, bottom, left (left to right, top to bottom, respectively)
        self.borders = [self.rows[0], "", self.rows[-1], ""]
        for row in self.rows:
            self.borders[RIGHT] += row[-1]
            self.borders[LEFT] += row[0]

        return self.borders

    @classmethod
    def rotate_borders(cls, borders):
        # top, right, bottom, left
        return [borders[LEFT][::-1], borders[TOP], borders[RIGHT][::-1], borders[BOTTOM]]

    @classmethod
    def flip_vertical_borders(cls, borders):
        # top, right, bottom, left
        return [borders[BOTTOM], borders[RIGHT][::-1], borders[TOP], borders[LEFT][::-1]]

    @classmethod
    def flip_horizontal_borders(cls, borders):
        # top, right, bottom, left
        return [borders[TOP][::-1], borders[LEFT], borders[BOTTOM][::-1], borders[RIGHT]]

    def rotate_clockwise(self):
        rotated = []
        for i in range(self.width):
            rotated.append("")

        for row in self.rows:
            for i in range(len(row)):
                rotated[i] = row[i] + rotated[i]
        self.rows = rotated
        self.borders = None
        self.get_borders()

    def flip(self):
        flipped = []

        for row in self.rows:
            flipped.append(row[::-1])

        self.rows = flipped
        self.borders = None
        self.get_borders()

    def get_no_borders(self):
        output_rows = []
        for row in self.rows[1:-1]:
            output_row = row[1:-1]
            output_rows.append(output_row)
        return output_rows

    def get_matching_dict(self, tile):
        """
        keep current tile fixed while orienting input tile
        return dictionary where key is side (TOP, RIGHT, BOTTOM, LEFT) and value is orientation count
        (0=as-is, 1=r90, 2=r180, 3=r270, 4=flip, 5=fr90, 6=fr180, 7=fr270)
        """
        matching_dict = {}
        my_borders = self.get_borders()
        their_borders = tile.get_borders()
        for my_side, their_side in [(TOP, BOTTOM), (RIGHT, LEFT), (BOTTOM, TOP), (LEFT, RIGHT)]:
            their_borders = tile.get_borders()
            for orientation_count in range(8):
                if orientation_count == 4:
                    # flip half-way through
                    their_borders = Tile.flip_horizontal_borders(their_borders)

                if my_borders[my_side] == their_borders[their_side]:
                    if my_side in matching_dict:
                        raise
                    matching_dict[my_side] = orientation_count

                their_borders = Tile.rotate_borders(their_borders)
        return matching_dict

    def apply_orientation_count(self, orientation_count):
        if orientation_count >= 4:
            self.flip()
        for i in range(orientation_count%4):
            self.rotate_clockwise()

    MONSTER = ["^..................#.",
               "^#....##....##....###",
               "^.#..#..#..#..#..#..."]

    def find_monster(self):
        monster_positions_set = set()
        monster_width = len(self.MONSTER[0])

        # find all places the middle match
        middle_match_dict = {} # keys are the row number, values are a list of columns
        pattern = re.compile(self.MONSTER[1])
        for row_index in range(1, len(self.rows) - 1):
            row = self.rows[row_index]
            for start_pos in range(0, len(row) - monster_width):
                m = pattern.search(row[start_pos:])
                if m:
                    if row_index not in middle_match_dict:
                        middle_match_dict[row_index] = set()
                    middle_match_dict[row_index].add(start_pos)

        # find all places the bottom matches with the middle
        bottom_match_dict = {} # keys are the row number, values are a list of columns
        pattern = re.compile(self.MONSTER[2])
        for middle_row_index, columns in middle_match_dict.items():
            row_index = middle_row_index+1
            row = self.rows[row_index]
            for start_pos in columns:
                m = pattern.search(row[start_pos:])
                if m:
                    if row_index not in bottom_match_dict:
                        bottom_match_dict[row_index] = set()
                    bottom_match_dict[row_index].add(start_pos)

        # find all places the top matches with the rest
        pattern = re.compile(self.MONSTER[0])
        for bottom_row_index, columns in bottom_match_dict.items():
            row_index = bottom_row_index-2
            row = self.rows[row_index]
            for start_pos in columns:
                m = pattern.search(row[start_pos:])
                if m:
                    monster_positions_set.add((row_index, start_pos))

        return monster_positions_set

    def add_monster(self, monster_pos):
        row_index = monster_pos[0]
        col_index = monster_pos[1]

        monster_height = len(self.MONSTER)
        monster_width = len(self.MONSTER[0])
        for monster_row in range(monster_height):
            for monster_col in range(monster_width):
                row = self.rows[row_index + monster_row]
                if self.MONSTER[monster_row][monster_col] == "#":
                    new_row = row[:col_index + monster_col-1] + "0" + row[col_index + monster_col:]
                    self.rows[row_index + monster_row] = new_row

    def get_water_rougness(self):
        roughness = 0
        for row in self.rows:
            for char in row:
                if char == "#":
                    roughness += 1
        return roughness