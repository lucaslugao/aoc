import sys
import math
import collections
import itertools


class Grid:
    def __init__(self, data):
        self.data = data
        self.h = len(self.data)
        self.w = len(self.data[0])

    def in_bounds(self, x, y):
        return 0 <= x < self.w and 0 <= y < self.h

    def at(self, x, y):
        if not self.in_bounds(x, y):
            return "."
        return self.data[y][x]

    def coords(self):
        for y in range(self.h):
            for x in range(self.w):
                yield x, y


def count_2f_antinodes(grid, freqs):
    anti = set()
    for f in freqs:
        for p1, p2 in itertools.combinations(freqs[f], 2):
            x1, y1 = p1
            x2, y2 = p2
            dx, dy = x2 - x1, y2 - y1
            a1x, a1y = x1 - dx, y1 - dy
            a2x, a2y = x2 + dx, y2 + dy
            if grid.in_bounds(a1x, a1y):
                anti.add((a1x, a1y))
            if grid.in_bounds(a2x, a2y):
                anti.add((a2x, a2y))
    return len(anti)


def count_line_antinodes(grid, freqs):
    anti = set()
    for f in freqs:
        for p1, p2 in itertools.combinations(freqs[f], 2):
            x1, y1 = p1
            x2, y2 = p2
            dx, dy = x2 - x1, y2 - y1
            gcd = math.gcd(dx, dy)
            dx //= gcd
            dy //= gcd
            p = (x1, y1)
            while grid.in_bounds(*p):
                anti.add(p)
                p = (p[0] + dx, p[1] + dy)
            p = (x1, y1)
            while grid.in_bounds(*p):
                anti.add(p)
                p = (p[0] - dx, p[1] - dy)
    return len(anti)


def get_freq_coords(grid):
    freqs = collections.defaultdict(set)
    for x, y in grid.coords():
        if grid.at(x, y) == ".":
            continue
        freqs[grid.at(x, y)].add((x, y))
    return freqs


if __name__ == "__main__":
    data = [line.strip() for line in sys.stdin]
    grid = Grid(data)
    freqs = get_freq_coords(grid)
    print(count_2f_antinodes(grid, freqs))
    print(count_line_antinodes(grid, freqs))
