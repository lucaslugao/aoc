import sys


SIZE = 71


class Grid:
    def __init__(self):
        self.grid = [[0 for _ in range(SIZE)] for _ in range(SIZE)]

    def add(self, x, y):
        self.grid[y][x] = 1

    def remove(self, x, y):
        self.grid[y][x] = 0

    def at(self, x, y):
        if 0 <= x < SIZE and 0 <= y < SIZE:
            return self.grid[y][x]
        return 1

    def points(self):
        for y in range(SIZE):
            for x in range(SIZE):
                yield (x, y), self.at(x, y)

    def shortest_path_length(self):
        queue = [((0, 0), 0)]
        visited = set(queue)
        while queue:
            (x, y), length = queue.pop(0)
            if (x, y) == (SIZE - 1, SIZE - 1):
                return length
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if (nx, ny) not in visited and self.at(nx, ny) == 0:
                    queue.append(((nx, ny), length + 1))
                    visited.add((nx, ny))
        return None

    def debug(self):
        for row in self.grid:
            print("".join(map(lambda x: "#" if x == 1 else ".", row)))


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


if __name__ == "__main__":
    coords = [tuple(map(int, line.strip().split(","))) for line in sys.stdin]
    g = Grid()
    for i, (x, y) in enumerate(coords):
        g.add(x, y)
        if i == 1023:
            print(g.shortest_path_length())

    uf = UnionFind()
    for (x, y), v in g.points():
        if v == 1:
            continue
        uf.find((x, y))
        for dx, dy in [(0, 1), (1, 0)]:
            if g.at(x + dx, y + dy) == 0:
                uf.union((x, y), (x + dx, y + dy))
    for x, y in reversed(coords):
        g.remove(x, y)
        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            if g.at(x + dx, y + dy) == 0:
                uf.union((x, y), (x + dx, y + dy))
        if uf.find((0, 0)) == uf.find((SIZE - 1, SIZE - 1)):
            print(f"{x},{y}")
            break
