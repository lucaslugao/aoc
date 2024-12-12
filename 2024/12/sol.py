import sys
import dataclasses
import itertools


class Grid:
    def __init__(self, data):
        self.data = data
        self.h = len(self.data)
        self.w = len(self.data[0]) if self.h > 0 else 0

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


class UnionFind:
    def __init__(self):
        self.parent = {}
        self.rank = {}

    def find(self, x):
        if x not in self.parent:
            self.parent[x] = x
            self.rank[x] = 0
            return x
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, x, y):
        root_x = self.find(x)
        root_y = self.find(y)
        if root_x == root_y:
            return
        if self.rank[root_x] < self.rank[root_y]:
            self.parent[root_x] = root_y
        elif self.rank[root_x] > self.rank[root_y]:
            self.parent[root_y] = root_x
        else:
            self.parent[root_x] = root_y
            self.rank[root_y] += 1

    def components(self):
        components = {}
        for x in self.parent:
            root = self.find(x)
            if root not in components:
                components[root] = []
            components[root].append(x)
        return components

    @staticmethod
    def from_grid(grid):
        uf = UnionFind()
        for x, y in grid.coords():
            uf.union((x, y), (x, y))
            if grid.at(x, y) == grid.at(x + 1, y):
                uf.union((x, y), (x + 1, y))
            if grid.at(x, y) == grid.at(x, y + 1):
                uf.union((x, y), (x, y + 1))
        return uf


@dataclasses.dataclass(frozen=True)
class Wall:
    pos: tuple[int, int]
    normal: tuple[int, int]

    def close_to(self, other):
        if self.normal != other.normal:
            return False
        if abs(self.pos[0] - other.pos[0]) == 1 and self.pos[1] == other.pos[1]:
            return True
        if abs(self.pos[1] - other.pos[1]) == 1 and self.pos[0] == other.pos[0]:
            return True
        return False


def get_component_perimeter(
    component: list[tuple[int, int]], grid: Grid
) -> set[tuple[int, int]]:
    perimeter = set()
    for x, y in component:
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            if grid.at(x + dx, y + dy) != grid.at(x, y):
                perimeter.add(Wall((x, y), (dx, dy)))
    return perimeter


def reduce_walls(perimeter: set[Wall]) -> set[Wall]:
    uf = UnionFind()
    for wall in perimeter:
        uf.union(wall, wall)
    for w1, w2 in itertools.combinations(perimeter, 2):
        if w1.close_to(w2):
            uf.union(w1, w2)
    return uf.components().keys()


def solve(components, grid):
    total1, total2 = 0, 0
    for component in components.values():
        perimeter = get_component_perimeter(component, grid)
        walls = reduce_walls(perimeter)
        total1 += len(component) * len(perimeter)
        total2 += len(component) * len(walls)
    return total1, total2


if __name__ == "__main__":
    grid_data = [line.strip() for line in sys.stdin]
    grid = Grid(grid_data)
    uf = UnionFind.from_grid(grid)
    components = uf.components()
    result1, result2 = solve(components, grid)
    print(result1)
    print(result2)
