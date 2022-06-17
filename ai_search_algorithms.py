# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import math
import sys
import time
from heapq import heappop, heappush

str_bfs = "BFS"
str_ucs = "UCS"
str_a_star = "A*"
steps = []
OFFSET = [[0, 1, -1, 0, 0, 0, 0, 1, 1, -1, -1, 1, 1, -1, -1, 0, 0, 0, 0],
          [0, 0, 0, 1, -1, 0, 0, 1, -1, 1, -1, 0, 0, 0, 0, 1, 1, -1, -1],
          [0, 0, 0, 0, 0, 1, -1, 0, 0, 0, 0, 1, -1, 1, -1, 1, -1, 1, -1]]


class BfsNode:
    def __init__(self, loc, parent, cost):
        self.loc = loc
        self.parent = parent
        self.cost = cost

    def __lt__(self, other):
        return self.cost < other.cost


def in_dimensions(dim, grid):
    if 0 <= grid[0] < dim[0] and 0 <= grid[1] < dim[1] and 0 <= grid[2] < dim[2]:
        return True
    return False


def bfs(grids, dim, start, end):
    root = BfsNode(start, None, 0)
    queue = []
    visited = set()

    queue.append(root)
    visited.add(root.loc)

    while len(queue) != 0:
        node = queue.pop(0)  # pop a node
        if node.loc == end:
            # target found
            path = [[node.loc, 1]]
            curr_parent = node.parent
            while curr_parent.parent is not None:
                path.insert(0, [curr_parent.loc, 1])
                curr_parent = curr_parent.parent

            path.insert(0, [curr_parent.loc, 0])
            return path, node.cost
        neighbors = grids.get(node.loc, [])

        for neighbor in neighbors:
            neighbor_coord = tuple([node.loc[0] + OFFSET[0][int(neighbor)], node.loc[1] + OFFSET[1][int(neighbor)],
                                    node.loc[2] + OFFSET[2][int(neighbor)]])
            if in_dimensions(dim, neighbor_coord) and neighbor_coord not in visited:
                visited.add(neighbor_coord)
                queue.append(BfsNode(neighbor_coord, node, node.cost + 1))

    return None, None


def ucs(grids, dim, start, end):
    root = BfsNode(start, None, 0)
    queue = []
    visited = set()
    cost_so_far = dict()

    heappush(queue, root)
    cost_so_far[root.loc] = 0

    while len(queue) != 0:
        node = heappop(queue)

        if node.loc in visited and cost_so_far[node.loc] < node.cost:
            continue

        if node.loc == end:
            # target found
            path = []
            curr_node = node
            while curr_node.parent is not None:
                path.insert(0, [curr_node.loc, curr_node.cost - curr_node.parent.cost])
                curr_node = curr_node.parent
            path.insert(0, [curr_node.loc, 0])
            return path, node.cost

        visited.add(node.loc)

        children = grids.get(node.loc, [])
        for child in children:
            child_coord = tuple([node.loc[0] + OFFSET[0][child], node.loc[1] + OFFSET[1][child],
                                 node.loc[2] + OFFSET[2][child]])
            if not in_dimensions(dim, child_coord):
                continue

            child_cost = cost_so_far[node.loc] + calculate_cost(child)  # calculate path cost from parent to child
            child_node = BfsNode(child_coord, node, child_cost)
            if child_coord not in visited and child_cost < cost_so_far.get(child_coord, sys.maxsize):
                heappush(queue, child_node)
                cost_so_far[child_coord] = child_cost

    return None, None


def calculate_cost(child):
    if 0 < child < 7:
        return 10
    elif 6 < child < 19:
        return 14
    return 0


def heuristic_func(point1, point2):
    x1, y1, z1 = point1
    x2, y2, z2 = point2
    return 9*math.sqrt(abs(x2-x1)**2 + abs(y2-y1)**2 + abs(z2-z1)**2)


def a_star(grids, dim, start, end):
    root = BfsNode(start, None, 0)
    queue = []
    visited = set()
    cost_so_far = dict()

    heappush(queue, root)
    cost_so_far[root.loc] = 0

    while len(queue) != 0:
        node = heappop(queue)

        if node.loc in visited and cost_so_far[node.loc] < node.cost:
            continue

        if node.loc == end:
            # target found
            path = []
            curr_node = node
            while curr_node.parent is not None:
                path.insert(0, [curr_node.loc, cost_so_far[curr_node.loc] - cost_so_far[curr_node.parent.loc]])
                curr_node = curr_node.parent
            path.insert(0, [curr_node.loc, 0])
            return path, cost_so_far[node.loc]

        visited.add(node.loc)

        children = grids.get(node.loc, [])
        for child in children:
            child_coord = tuple([node.loc[0] + OFFSET[0][child], node.loc[1] + OFFSET[1][child],
                                 node.loc[2] + OFFSET[2][child]])
            if not in_dimensions(dim, child_coord):
                continue

            child_cost = cost_so_far[node.loc] + calculate_cost(child)  # calculate path cost from parent to child
            if child_coord not in visited and child_cost < cost_so_far.get(child_coord, sys.maxsize):
                cost_so_far[child_coord] = child_cost
                child_cost += heuristic_func(node.loc, child_coord)
                child_node = BfsNode(child_coord, node, child_cost)
                heappush(queue, child_node)

    return None, None


def read_file():
    # with open('input26.txt') as fp:
    with open('./Testcases/input/input26.txt') as fp:
        algo = fp.readline().rstrip()
        dim = fp.readline().split()
        start = fp.readline().split()
        end = fp.readline().split()
        grids = dict()

        for line in fp:
            temp = line.split()

            key = []
            value = []
            for i in range(len(temp)):
                if i < 3:
                    key.append(int(temp[i]))
                else:
                    value.append(int(temp[i]))

            grids[tuple(key)] = value

        dim = [int(num) for num in dim]
        start = tuple([int(num) for num in start])
        end = tuple([int(num) for num in end])
        cost = None

        start_time = time.time()
        if algo == str_bfs:
            path, cost = bfs(grids, dim, start, end)
        elif algo == str_ucs:
            path, cost = ucs(grids, dim, start, end)
        elif algo == str_a_star:
            path, cost = a_star(grids, dim, start, end)
        else:
            print("Wrong test case")
        end_time = time.time()
        run_time = end_time-start_time
        print(run_time)

        # with open('output.txt', 'w') as op:
        with open('./Testcases/output/output26.txt', 'w') as op:
            write_output(op, cost, path)


def write_output(op, cost, path):
    if cost is None:
        op.write("FAIL")
        return

    op.write(str(cost) + "\n")
    op.write(str(len(path)) + "\n")
    for line in path:
        op.write(str(line[0][0]) + " ")
        op.write(str(line[0][1]) + " ")
        op.write(str(line[0][2]) + " ")
        op.write(str(line[1]) + "\n")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    read_file()
