from collections import Counter
from copy import copy
from main import BaseProcessor

class D9Processor(BaseProcessor):

    def setup(self):
        grid = []
        with open(self.path, "r") as f:
            for line in f:
                line = line.strip()
                row = []
                for char in line:
                    row.append(int(char))
                grid.append(row)

        width = len(row)
        height = len(grid)
        lows = []
        low_values = []
        for i in range(len(grid)):
            for j in range(len(grid[i])):
                cur = grid[i][j]
                # top
                if i > 0 and grid[i-1][j] <= cur:
                    continue

                # left
                if j > 0 and grid[i][j-1] <= cur:
                    continue

                # right
                if j < width - 1 and grid[i][j+1] <= cur:
                    continue

                # bottom
                if i < height - 1 and grid[i+1][j] <= cur:
                    continue
                lows.append((i,j))
                low_values.append(cur)

        total = 0
        for value in low_values:
            total += value + 1
        print(f"part1: {total}")

        basins = []
        for low in lows:
            points = [low]
            basin_size = 1
            basin = set()

            while points:
                new_points = []
                for point in points:
                    i = point[0]
                    j = point[1]

                    # top
                    new_point = (i-1,j)
                    if i > 0 and new_point not in basin and grid[i - 1][j] != 9:
                        basin.add(new_point)
                        new_points.append(new_point)

                    # left
                    new_point = (i, j-1)
                    if j > 0 and new_point not in basin and grid[i][j - 1] != 9:
                        basin.add(new_point)
                        new_points.append(new_point)

                    # right
                    new_point = (i, j+1)
                    if j < width - 1 and new_point not in basin and grid[i][j + 1] != 9:
                        basin.add(new_point)
                        new_points.append(new_point)

                    # bottom
                    new_point = (i+1, j)
                    if i < height - 1 and new_point not in basin and grid[i + 1][j] != 9:
                        basin.add(new_point)
                        new_points.append(new_point)

                points = new_points
            basins.append(basin)

        largest_basin_indexes = set()
        largest_basin_sizes = []
        part2 = 1
        cur_largest_value = 0
        for loop_count in range(3):
            cur_largest_value = 0
            cur_largest_index = -1
            for i, basin in enumerate(basins):
                if len(basin) > cur_largest_value and i not in largest_basin_indexes:
                    cur_largest_value = len(basin)
                    cur_largest_index = i
            largest_basin_indexes.add(cur_largest_index)
            largest_basin_sizes.append(cur_largest_value)
            part2 *= cur_largest_value
        print(f"part2: {part2}")


    def run1(self):
        self.setup()
        pass


    def run2(self):
        pass

