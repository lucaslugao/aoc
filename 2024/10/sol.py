import sys


class Grid:
    def __init__(self, data):
        self.data = data
        self.h = len(self.data)
        self.w = len(self.data[0])

    def at(self, x, y):
        if x < 0 or x >= self.w or y < 0 or y >= self.h:
            return -100
        return self.data[y][x]

    def coords(self):
        for y in range(self.h):
            for x in range(self.w):
                yield x, y

    def count_reachable(self, start, target=9):
        visited = set()
        stack = [start]
        count = 0
        while stack:
            x, y = stack.pop()
            if (x, y) in visited:
                continue
            visited.add((x, y))
            if self.at(x, y) == target:
                count += 1
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                if self.at(x + dx, y + dy) == self.at(x, y) + 1:
                    stack.append((x + dx, y + dy))
        return count

    def count_trails(self, start, target=9):
        def dfs(x, y, visited):
            if (x, y) in visited:
                return 0
            visited = visited | {(x, y)}
            if self.at(x, y) == target:
                return 1
            count = 0
            for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                if self.at(x + dx, y + dy) == self.at(x, y) + 1:
                    count += dfs(x + dx, y + dy, visited)
            return count

        return dfs(*start, set())


if __name__ == "__main__":
    grid = Grid([[int(a) for a in line.strip()] for line in sys.stdin if line.strip()])
    total = 0
    total2 = 0
    for x, y in grid.coords():
        if grid.at(x, y) == 0:
            total += grid.count_reachable((x, y))
            total2 += grid.count_trails((x, y))
    print(total)
    print(total2)
