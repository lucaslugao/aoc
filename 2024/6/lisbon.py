"""
This solution is messy and slow, but it was done in a airplane from Paris to
Lisbon! I will try to improve it later, but it was fun to do it while flying.
"""
import sys


class Grid:
    def __init__(self, data):
        self.data = [list(r) for r in data]
        self.h = len(self.data)
        self.w = len(self.data[0])

    def inside(self, x, y):
        return x >= 0 and x < self.w and y >= 0 and y < self.h

    def at(self, x, y):
        if not self.inside(x, y):
            return "."
        return self.data[y][x]

    def edit(self, x, y, v):
        if x < 0 or x >= self.w or y < 0 or y >= self.h:
            return
        self.data[y][x] = v

    def coords(self):
        for y in range(self.h):
            for x in range(self.w):
                yield x, y

    def debug(self, states, temp):
        print("--")
        o = {}
        for p, v in states:
            o[p] = v
        for y in range(self.h):
            for x in range(self.w):
                if (x, y) == temp:
                    print("T", end="")
                elif (x, y) in o:
                    print(o[(x, y)], end="")
                else:
                    print(self.data[y][x], end="")
            print()


TURN = {
    ">": "v",
    "v": "<",
    "<": "^",
    "^": ">",
}
DELTA = {
    ">": (1, 0),
    "v": (0, 1),
    "<": (-1, 0),
    "^": (0, -1),
}


def add(p1, p2):
    return tuple([c1 + c2 for c1, c2 in zip(p1, p2)])


def solve1(grid, state):
    points = set()
    while True:
        p, v = state
        points.add(p)
        np = add(p, DELTA[v])
        if not grid.inside(*np):
            break
        if grid.at(*np) == ".":
            state = (np, v)
        else:
            state = (p, TURN[v])
    return len(points)


def solve2(grid, state):
    snapshot = 0
    tried = set()
    temp = None
    path = []
    c = 0
    while True:
        if temp is not None and state in path:
            print("Loop with", temp, " c =", c, " s =", snapshot)
            c += 1
            path = path[:snapshot]
            state = path[-1]
            snapshot = 0
            temp = None
        path.append(state)
        p, v = state
        np = add(p, DELTA[v])
        if not grid.inside(*np):
            if snapshot > 0:
                path = path[:snapshot]
                state = path[-1]
                snapshot = 0
                temp = None
                continue
            else:
                break
        if grid.at(*np) == "." and np != temp:
            if np in tried or snapshot > 0:
                state = (np, v)
            elif snapshot == 0:
                tried.add(np)
                temp = np
                snapshot = len(path)
                state = (p, TURN[v])
        else:
            state = (p, TURN[v])
    return c


if __name__ == "__main__":
    grid = Grid([line.strip() for line in sys.stdin if line.strip()])
    state = None
    for x, y in grid.coords():
        v = grid.at(x, y)
        if v not in ".#":
            state = ((x, y), v)
            grid.edit(x, y, ".")
            break
    print(solve1(grid, state))
    print(solve2(grid, state))
