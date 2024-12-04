import sys


class Grid:
    def __init__(self, data):
        self.data = data
        self.w = len(data)
        self.h = len(data[0])

    def at(self, x, y):
        if x < 0 or x >= self.w or y < 0 or y >= self.h:
            return "."
        return self.data[y][x]

    def coords(self):
        for y in range(self.h):
            for x in range(self.w):
                yield x, y


def count_xmas(grid):
    neigh = [
        (0, 1),
        (0, -1),
        (1, 0),
        (-1, 0),
        (1, 1),
        (-1, -1),
        (1, -1),
        (-1, 1),
    ]

    def has_xmas_at(x, y, dx, dy):
        for i, c in enumerate("XMAS"):
            if grid.at(x + i * dx, y + i * dy) != c:
                return False
        return True

    count = 0

    for x, y in grid.coords():
        for dx, dy in neigh:
            if has_xmas_at(x, y, dx, dy):
                count += 1

    return count


def count_x_mas(grid):
    def coords_form_mas(coords):
        return "".join(grid.at(x, y) for x, y in coords) in {"MAS", "SAM"}

    def has_cross_at(x, y):
        return all(
            coords_form_mas(diagonal)
            for diagonal in [
                [(x - 1, y - 1), (x, y), (x + 1, y + 1)],
                [(x - 1, y + 1), (x, y), (x + 1, y - 1)],
            ]
        )

    count = 0

    for x, y in grid.coords():
        if has_cross_at(x, y):
            count += 1

    return count


if __name__ == "__main__":
    grid = Grid([line.strip() for line in sys.stdin if line.strip()])

    print(count_xmas(grid))
    print(count_x_mas(grid))
