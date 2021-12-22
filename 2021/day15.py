from collections import Counter
from copy import copy, deepcopy
from main import BaseProcessor
from queue import SimpleQueue
import sys
from threading import Thread, Lock


class D15Processor(BaseProcessor):

    def setup(self):
        pass

    def run1(self):
        nodes = []
        init_graph = {}
        with open(self.path, "r") as f:
            rows = []
            for y, line in enumerate(f):
                row = []
                line = line.strip()
                for x, char in enumerate(line):
                    node_name = f"{x}_{y}"
                    nodes.append(node_name)
                    init_graph[node_name] = {}
                    row.append(int(char))
                rows.append(row)
        width = len(rows[0])
        height = len(rows)

        for y, row in enumerate(rows):
            for x in range(len(row)):
                node_name = f"{x}_{y}"
                if x < width - 1:
                    init_graph[node_name][f"{x + 1}_{y}"] = row[x + 1]
                if y < height - 1:
                    init_graph[node_name][f"{x}_{y + 1}"] = rows[y + 1][x]
                if x > 0:
                    init_graph[node_name][f"{x - 1}_{y}"] = row[x - 1]
                if y > 0:
                    init_graph[node_name][f"{x}_{y - 1}"] = rows[y - 1][x]
        graph = Graph(nodes, init_graph, width, height)
        previous_nodes, shortest_path = dijkstra_algorithm(graph, "0_0")

        last_node_name = f"{height - 1}_{width - 1}"
        print(f"part1: {shortest_path[last_node_name]}")
        print_result(previous_nodes, shortest_path, "0_0", last_node_name)
        total = 0
        cur_node_name = last_node_name
        while cur_node_name != "0_0":
            x, y = cur_node_name.split("_")
            x = int(x)
            y = int(y)
            total += rows[y][x]
            cur_node_name = previous_nodes[cur_node_name]
        print(f"part1b: {total}")

    def run2(self):
        with open(self.path, "r") as f:
            rows = []
            for y, line in enumerate(f):
                row = []
                line = line.strip()
                for x, char in enumerate(line):
                    row.append(int(char))
                rows.append(row)
        grid = Grid(rows)
        rows = grid.get_rows(5)
        height = len(rows)
        width = len(rows[0])

        nodes = []
        init_graph = {}
        for y in range(height):
            for x in range(width):
                node_name = f"{x}_{y}"
                nodes.append(node_name)
                init_graph[node_name] = {}
                if x < width - 1:
                    init_graph[node_name][f"{x + 1}_{y}"] = rows[y][x+1]
                if y < height - 1:
                    init_graph[node_name][f"{x}_{y + 1}"] = rows[y+1][x]
                if x > 0:
                    init_graph[node_name][f"{x - 1}_{y}"] = rows[y][x-1]
                if y > 0:
                    init_graph[node_name][f"{x}_{y - 1}"] = rows[y-1][x]
        graph = Graph(nodes, init_graph, width, height)
        previous_nodes, shortest_path = dijkstra_algorithm(graph, "0_0")

        last_node_name = f"{height - 1}_{width - 1}"
        print(f"part2: {shortest_path[last_node_name]}")
        """
        print_result(previous_nodes, shortest_path, "0_0", last_node_name)
        total = 0
        cur_node_name = last_node_name
        while cur_node_name != "0_0":
            total += grid.get_value(cur_node_name)
            cur_node_name = previous_nodes[cur_node_name]
        print(f"part2: {total}")
        """

class Grid:
    def __init__(self, base_rows):
        self.rows = list(base_rows)
        self.height = len(self.rows)
        self.width = len(self.rows[0])

    def get_value(self, node_name):
        x, y = node_name.split("_")
        x = int(x)
        y = int(y)
        return self.get_value_coord(x, y)

    def get_value_coord(self, x, y):
        base_value = self.rows[y%self.width][x%self.width]
        value = base_value + self.get_increase(x, y)
        if value > 9:
            value -= 9
        return value

    def get_increase(self, x, y):
        return int(x/self.width) + int(y/self.height)

    def get_rows(self, multiplier):
        rows = []
        for y in range(self.height * multiplier):
            row = []
            for x in range(self.width*multiplier):
                row.append(self.get_value_coord(x, y))
            rows.append(row)
        return rows


def print_result(previous_nodes, shortest_path, start_node, target_node):
    path = []
    node = target_node

    while node != start_node:
        path.append(node)
        node = previous_nodes[node]

    # Add the start node manually
    path.append(start_node)

    print("We found the following best path with a value of {}.".format(shortest_path[target_node]))
    print(" -> ".join(reversed(path)))


def dijkstra_algorithm(graph, start_node):
    unvisited_nodes = list(graph.get_nodes())

    # We'll use this dict to save the cost of visiting each node and update it as we move along the graph
    shortest_path = {}

    # We'll use this dict to save the shortest known path to a node found so far
    previous_nodes = {}

    # We'll use max_value to initialize the "infinity" value of the unvisited nodes
    #max_value = sys.maxsize
    for node in unvisited_nodes:
        shortest_path[node] = float('inf')
    # However, we initialize the starting node's value with 0
    shortest_path[start_node] = 0
    priority_unvisited_nodes = set([start_node])

    # The algorithm executes until we visit all nodes
    while unvisited_nodes:
        # The code block below finds the node with the lowest score
        """
        current_min_node = unvisited_nodes[0]
        for node in unvisited_nodes[1:]:  # Iterate over the nodes
            if shortest_path[node] < shortest_path[current_min_node]:
                current_min_node = node
        """
        temp_priority_unvisited_nodes = set()
        if priority_unvisited_nodes:
            current_min_node = priority_unvisited_nodes.pop()
        else:
            current_min_node = unvisited_nodes[0]
        while priority_unvisited_nodes:  # Iterate over the nodes
            node = priority_unvisited_nodes.pop()
            if shortest_path[node] < shortest_path[current_min_node]:
                temp_priority_unvisited_nodes.add(current_min_node)
                current_min_node = node
            else:
                temp_priority_unvisited_nodes.add(node)
        priority_unvisited_nodes = temp_priority_unvisited_nodes

        # The code block below retrieves the current node's neighbors and updates their distances
        neighbors = graph.get_outgoing_edges(current_min_node)
        for neighbor in neighbors:
            tentative_value = shortest_path[current_min_node] + graph.value(current_min_node, neighbor)
            if tentative_value < shortest_path[neighbor]:
                shortest_path[neighbor] = tentative_value
                # We also update the best path to the current node
                previous_nodes[neighbor] = current_min_node
                priority_unvisited_nodes.add(neighbor)

        # After visiting its neighbors, we mark the node as "visited"
        unvisited_nodes.remove(current_min_node)

    return previous_nodes, shortest_path


class Graph(object):
    def __init__(self, nodes, init_graph, width, height):
        self.nodes = nodes
        self.graph = dict(init_graph)
        self.width = width
        self.height = height

    def construct_graph(self, nodes, init_graph):
        '''
        This method makes sure that the graph is symmetrical. In other words, if there's a path from node A to B with a value V, there needs to be a path from node B to node A with a value V.
        '''
        graph = {}
        for node in nodes:
            graph[node] = {}

        graph.update(init_graph)

        for node, edges in graph.items():
            for adjacent_node, value in edges.items():
                if node not in graph[adjacent_node]:
                    graph[adjacent_node][node] = value

        return graph

    def get_nodes(self):
        "Returns the nodes of the graph."
        return self.nodes

    def get_outgoing_edges(self, node):
        "Returns the neighbors of a node."
        connections = []

        '''
        for out_node in self.nodes:
            if self.graph[node].get(out_node, False) != False:
                connections.append(out_node)
        '''
        x, y = node.split("_")
        x = int(x)
        y = int(y)
        if x > 0:
            connections.append(f"{x-1}_{y}")
        if x < self.width - 1:
            connections.append(f"{x+1}_{y}")
        if y > 0:
            connections.append(f"{x}_{y-1}")
        if y < self.height - 1:
            connections.append(f"{x}_{y+1}")

        return connections

    def value(self, node1, node2):
        "Returns the value of an edge between two nodes."
        return self.graph[node1][node2]