import sys
from typing import Set
import time

DIR_TO_COMPLEX = {
    ">": 1,
    "<": -1,
    "^": -1j,
    "v": 1j,
}


class Grid:
    width: int
    height: int

    walls: Set[complex]
    boxes: Set[complex]

    robot: complex

    def __init__(self, grid):
        self.width = len(grid[0])
        self.height = len(grid)

        self.walls = set()
        self.boxes = set()

        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                pos = x + y * 1j
                if cell == "#":
                    self.walls.add(pos)
                elif cell == "O":
                    self.boxes.add(pos)
                elif cell == "@":
                    self.robot = pos

    def move_box(self, box, dir):
        new_pos = box + dir
        if new_pos in self.walls:
            return False
        if new_pos in self.boxes and not self.move_box(new_pos, dir):
            return False
        self.boxes.remove(box)
        self.boxes.add(new_pos)
        return True

    def move_robot(self, dir):
        new_pos = self.robot + dir
        if new_pos in self.walls:
            return False
        if new_pos in self.boxes and not self.move_box(new_pos, dir):
            return False
        self.robot = new_pos
        return True

    def show(self):
        for y in range(self.height):
            for x in range(self.width):
                pos = x + y * 1j
                if pos in self.walls:
                    print("#", end="")
                elif pos in self.boxes:
                    print("O", end="")
                elif pos == self.robot:
                    print("@", end="")
                else:
                    print(" ", end="")
            print()

    def checksum(self):
        return sum(int(p.real + p.imag * 100) for p in self.boxes)


class DoubleGrid:
    width: int
    height: int

    walls: Set[complex]
    boxes: Set[complex]
    robot: complex

    def __init__(self, grid):
        self.width = len(grid[0]) * 2
        self.height = len(grid)

        self.walls = set()
        self.boxes = set()

        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                pos = 2 * x + y * 1j
                if cell == "#":
                    self.walls.add(pos)
                    self.walls.add(pos + 1)
                elif cell == "O":
                    self.boxes.add(pos)
                elif cell == "@":
                    self.robot = pos

    def robot_hit_box(self, pos):
        if pos in self.boxes:
            yield pos
        if pos - 1 in self.boxes:
            yield pos - 1

    def box_hit_box(self, pos):
        if pos in self.boxes:
            yield pos
        if pos - 1 in self.boxes:
            yield pos - 1
        if pos + 1 in self.boxes:
            yield pos + 1

    def move_box(self, box, dir, do=False):
        new_pos = box + dir
        if new_pos in self.walls or new_pos + 1 in self.walls:
            return False
        for box2 in self.box_hit_box(new_pos):
            if box2 == box:
                continue
            if not self.move_box(box2, dir, do):
                return False
        if do:
            self.boxes.remove(box)
            self.boxes.add(new_pos)
        return True

    def move_robot(self, dir):
        new_pos = self.robot + dir
        if new_pos in self.walls:
            return False
        for box in self.robot_hit_box(new_pos):
            if self.move_box(box, dir):
                self.move_box(box, dir, True)
            else:
                return False
        self.robot = new_pos
        return True

    def show(self):
        for y in range(self.height):
            for x in range(self.width):
                pos = x + y * 1j
                if pos in self.walls:
                    print("#", end="")
                elif pos in self.boxes:
                    print("[", end="")
                elif pos - 1 in self.boxes:
                    print("]", end="")
                elif pos == self.robot:
                    print("@", end="")
                else:
                    print(" ", end="")
            print()

    def checksum(self):
        return sum(int(p.real + p.imag * 100) for p in self.boxes)


if __name__ == "__main__":
    data = sys.stdin.read()
    grid_data, moves = data.split("\n\n")
    grid_data = grid_data.splitlines()

    grid = Grid(grid_data)
    dgrid = DoubleGrid(grid_data)
    for move in moves:
        if move not in DIR_TO_COMPLEX:
            continue
        dir = DIR_TO_COMPLEX[move]
        grid.move_robot(dir)
        dgrid.move_robot(dir)

    print(grid.checksum())
    print(dgrid.checksum())
