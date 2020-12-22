from main import BaseProcessor

class D17Processor(BaseProcessor):
    def run_all(self):
        self.base_run(path_suffix="example")
        #self.base_run(path_suffix="example2")
        #self.base_run(path_suffix="example3")
        #self.base_run(path_suffix="example4")
        self.base_run()

    def run1(self):
        cubes = Cubes()
        with open(self.path, "r") as f:
            z = 0
            y = -1
            for line in f:
                line = line.strip()
                x = -1
                for char in line:
                    if char == "#":
                        cubes.add_cube(x, y, z, True)
                    x += 1
                y += 1

        cubes.print_state()
        for i in range(6):
            cubes.cycle()
        print(f"part1: ")

    def run2(self):
        cubes = Cubes4()
        with open(self.path, "r") as f:
            z = 0
            w = 0
            y = -1
            for line in f:
                line = line.strip()
                x = -1
                for char in line:
                    if char == "#":
                        cubes.add_cube(x, y, z, w, True)
                    x += 1
                y += 1

        cubes.print_state()
        for i in range(6):
            cubes.cycle()
        print(f"part1: ")


class Cubes4:
    def __init__(self):
        self.coords = {}
        self.cubes_set = set()
        self.cycle_number = 0
        self.num_active = 0

    def add_cube(self, x, y, z, w, active):
        if x not in self.coords:
            self.coords[x] = {}
        if y not in self.coords[x]:
            self.coords[x][y] = {}
        if z not in self.coords[x][y]:
            self.coords[x][y][z] = {}
        if w not in self.coords[x][y][z]:
            cube = Cube4(x, y, z, w, self, active)
            self.cubes_set.add(cube)
            self.coords[x][y][z][w] = cube
        else:
            cube = self.coords[x][y][z][w]
            if not cube.is_active() and active:
                cube.state = True
                cube.add_neighbors()
        return cube

    def cycle(self):
        self.cycle_number += 1
        for cube in self.cubes_set:
            cube.cycle()
        self.num_active = 0
        for cube in list(self.cubes_set):
            cube.commit_next_state()
            if cube.is_active():
                self.num_active += 1
        self.print_state()

    def print_state(self):
        xs = set()
        ys = set()
        zs = set()
        ws = set()
        for cube in self.cubes_set:
            if cube.is_active():
                xs.add(cube.x)
                ys.add(cube.y)
                zs.add(cube.z)
                ws.add(cube.w)

        xmin = min(list(xs))
        xmax = max(list(xs))
        ymin = min(list(ys))
        ymax = max(list(ys))
        zs = list(zs)
        zs.sort()
        ws = list(ws)
        ws.sort()
        print(f"@ cycle #{self.cycle_number} @")
        for z in zs:
            for w in ws:
                print(f"z={z} w={w}")
                is_active = False
                for y in range(ymin, ymax+1):
                    #print(f"y={y}: ", end="")
                    for x in range(xmin, xmax+1):
                        if x in self.coords:
                            if y in self.coords[x]:
                                if z in self.coords[x][y]:
                                    if w in self.coords[x][y][z]:
                                        is_active = self.coords[x][y][z][w].is_active()
                        if is_active:
                            print("#", end="")
                        else:
                            print(".", end="")
                    print("")
                print("")
            print("")
        print(f"num active: {self.num_active}")

class Cube4:
    def __init__(self, x, y, z, w, cubes_obj, active):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.cubes_obj = cubes_obj
        self.neighbors_added = False
        self.neighbors = set()
        if active:
            self.state = True
            self.add_neighbors()
        else:
            self.state = False

    def is_active(self):
        return self.state

    def add_neighbors(self, ):
        if self.neighbors_added:
            return

        for _x in [-1, 0, 1]:
            for _y in [-1, 0, 1]:
                for _z in [-1, 0, 1]:
                    for _w in [-1, 0, 1]:
                        if _x == 0 and _y == 0 and _z == 0 and _w == 0:
                            continue

                        x = self.x + _x
                        y = self.y + _y
                        z = self.z + _z
                        w = self.w + _w
                        neighbor = self.cubes_obj.add_cube(x, y, z, w, False)
                        self.neighbors.add(neighbor)
        self.neighbors_added = True

    def get_num_active_neighbors(self):
        num_active = 0
        if self.neighbors_added:
            for neighbor in self.neighbors:
                if neighbor.is_active():
                    num_active += 1
        else:
            for _x in [-1, 0, 1]:
                for _y in [-1, 0, 1]:
                    for _z in [-1, 0, 1]:
                        for _w in [-1, 0, 1]:
                            if _x == 0 and _y == 0 and _z == 0 and _w == 0:
                                continue
                            x = self.x + _x
                            y = self.y + _y
                            z = self.z + _z
                            w = self.w + _w
                            if x in self.cubes_obj.coords:
                                if y in self.cubes_obj.coords[x]:
                                    if z in self.cubes_obj.coords[x][y]:
                                        if w in self.cubes_obj.coords[x][y][z]:
                                            neighbor = self.cubes_obj.coords[x][y][z][w]
                                            if neighbor.is_active():
                                                num_active += 1
        return num_active

    def cycle(self):
        num_active = self.get_num_active_neighbors()

        if self.is_active():
            if num_active == 2 or num_active == 3:
                self.next_state = True
            else:
                self.next_state = False
        else:
            if num_active == 3:
                self.next_state = True
            else:
                self.next_state = False

    def commit_next_state(self):
        self.state = self.next_state
        if self.is_active():
            self.add_neighbors()




class Cubes:
    def __init__(self):
        self.coords = {}
        self.cubes_set = set()
        self.cycle_number = 0
        self.num_active = 0

    def add_cube(self, x, y, z, active):
        if x not in self.coords:
            self.coords[x] = {}
        if y not in self.coords[x]:
            self.coords[x][y] = {}
        if z not in self.coords[x][y]:
            cube = Cube(x, y, z, self, active)
            self.cubes_set.add(cube)
            self.coords[x][y][z] = cube
        else:
            cube = self.coords[x][y][z]
            if not cube.is_active() and active:
                cube.state = True
                cube.add_neighbors()
        return cube

    def cycle(self):
        self.cycle_number += 1
        for cube in self.cubes_set:
            cube.cycle()
        self.num_active = 0
        for cube in list(self.cubes_set):
            cube.commit_next_state()
            if cube.is_active():
                self.num_active += 1
        self.print_state()

    def print_state(self):
        xs = set()
        ys = set()
        zs = set()
        for cube in self.cubes_set:
            if cube.is_active():
                xs.add(cube.x)
                ys.add(cube.y)
                zs.add(cube.z)

        xmin = min(list(xs))
        xmax = max(list(xs))
        ymin = min(list(ys))
        ymax = max(list(ys))
        zs = list(zs)
        zs.sort()
        print(f"@ cycle #{self.cycle_number} @")
        for z in zs:
            print(f"z={z}")
            is_active = False
            for y in range(ymin, ymax+1):
                #print(f"y={y}: ", end="")
                for x in range(xmin, xmax+1):
                    if x in self.coords:
                        if y in self.coords[x]:
                            if z in self.coords[x][y]:
                                is_active = self.coords[x][y][z].is_active()
                    if is_active:
                        print("#", end="")
                    else:
                        print(".", end="")
                print("")
            print("")
        print(f"num active: {self.num_active}")

class Cube:
    def __init__(self, x, y, z, cubes_obj, active):
        self.x = x
        self.y = y
        self.z = z
        self.cubes_obj = cubes_obj
        self.neighbors_added = False
        self.neighbors = set()
        if active:
            self.state = True
            self.add_neighbors()
        else:
            self.state = False

    def is_active(self):
        return self.state

    def add_neighbors(self, ):
        if self.neighbors_added:
            return

        for coord in [(-1, -1, -1), (-1, -1,  0), (-1, -1,  1), (-1, 0, -1), (-1,  0,  0), (-1,  0,  1), (-1,  1, -1), (-1,  1,  0), (-1,  1,  1),
                      ( 0, -1, -1), ( 0, -1,  0), ( 0, -1,  1), ( 0, 0, -1),               ( 0,  0,  1), ( 0,  1, -1), ( 0,  1,  0), ( 0,  1,  1),
                      ( 1, -1, -1), ( 1, -1,  0), ( 1, -1,  1), ( 1, 0, -1), ( 1,  0,  0), ( 1,  0,  1), ( 1,  1, -1), ( 1,  1,  0), ( 1,  1,  1)]:
            _x = coord[0]
            _y = coord[1]
            _z = coord[2]
            x = self.x + _x
            y = self.y + _y
            z = self.z + _z
            neighbor = self.cubes_obj.add_cube(x, y, z, False)
            self.neighbors.add(neighbor)
        self.neighbors_added = True

    def get_num_active_neighbors(self):
        num_active = 0
        if self.neighbors_added:
            for neighbor in self.neighbors:
                if neighbor.is_active():
                    num_active += 1
        else:
            for coord in [(-1, -1, -1), (-1, -1,  0), (-1, -1,  1), (-1, 0, -1), (-1,  0,  0), (-1,  0,  1), (-1,  1, -1), (-1,  1,  0), (-1,  1,  1),
                          ( 0, -1, -1), ( 0, -1,  0), ( 0, -1,  1), ( 0, 0, -1),               ( 0,  0,  1), ( 0,  1, -1), ( 0,  1,  0), ( 0,  1,  1),
                          ( 1, -1, -1), ( 1, -1,  0), ( 1, -1,  1), ( 1, 0, -1), ( 1,  0,  0), ( 1,  0,  1), ( 1,  1, -1), ( 1,  1,  0), ( 1,  1,  1)]:
                _x = coord[0]
                _y = coord[1]
                _z = coord[2]
                x = self.x + _x
                y = self.y + _y
                z = self.z + _z
                if x in self.cubes_obj.coords:
                    if y in self.cubes_obj.coords[x]:
                        if z in self.cubes_obj.coords[x][y]:
                            neighbor = self.cubes_obj.coords[x][y][z]
                            if neighbor.is_active():
                                num_active += 1
        return num_active

    def cycle(self):
        num_active = self.get_num_active_neighbors()

        if self.is_active():
            if num_active == 2 or num_active == 3:
                self.next_state = True
            else:
                self.next_state = False
        else:
            if num_active == 3:
                self.next_state = True
            else:
                self.next_state = False

    def commit_next_state(self):
        self.state = self.next_state
        if self.is_active():
            self.add_neighbors()
