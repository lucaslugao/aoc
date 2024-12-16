from heapq import heappop, heappush
import dataclasses
import collections
import sys
from typing import List, Tuple, Set, Dict


@dataclasses.dataclass(frozen=True, eq=True, order=True)
class Point:
    x: int
    y: int


@dataclasses.dataclass(frozen=True, eq=True, order=True)
class Direction:
    dx: int
    dy: int


TURN_CW = {
    Direction(1, 0): Direction(0, 1),  # E -> S
    Direction(0, 1): Direction(-1, 0),  # S -> W
    Direction(-1, 0): Direction(0, -1),  # W -> N
    Direction(0, -1): Direction(1, 0),  # N -> E
}

TURN_CCW = {
    Direction(1, 0): Direction(0, -1),  # E -> N
    Direction(0, 1): Direction(1, 0),  # S -> E
    Direction(-1, 0): Direction(0, 1),  # W -> S
    Direction(0, -1): Direction(-1, 0),  # N -> W
}


@dataclasses.dataclass(frozen=True, eq=True, order=True)
class State:
    pos: Point
    dir: Direction

    def forward(self: "State") -> "State":
        return State(
            Point(self.pos.x + self.dir.dx, self.pos.y + self.dir.dy),
            self.dir,
        )

    def back(self: "State") -> "State":
        return State(
            Point(self.pos.x - self.dir.dx, self.pos.y - self.dir.dy),
            self.dir,
        )

    def turn(self: "State") -> List["State"]:
        return [State(self.pos, nd) for nd in (TURN_CW[self.dir], TURN_CCW[self.dir])]


class Grid:
    def __init__(self, lines):
        self.w, self.h = len(lines[0]), len(lines)
        self.start = None
        self.end = None
        self.data: Set[Point] = set()
        for y, row in enumerate(lines):
            for x, ch in enumerate(row):
                if ch == "#":
                    continue
                p = Point(x, y)
                self.data.add(p)
                if ch == "S":
                    self.start = p
                elif ch == "E":
                    self.end = p
        self.cost: Dict[State, int] = {}
        self.min_cost = None

    def solve(self) -> bool:
        start_dir = Direction(1, 0)  # Facing east first
        start_state = State(self.start, start_dir)
        self.cost[start_state] = 0

        pq: List[Tuple[int, State]] = []
        heappush(pq, (0, start_state))
        visited = set()
        while pq:
            cost, state = heappop(pq)
            if state.pos == self.end:
                self.min_cost = cost
                return True

            if state in visited:
                continue
            visited.add(state)

            # Prune if we have already found a better path
            if state in self.cost and self.cost[state] < cost:
                continue

            # Turn
            for next_state in state.turn():
                if next_state not in self.cost or cost + 1000 < self.cost[next_state]:
                    self.cost[next_state] = cost + 1000
                    heappush(pq, (cost + 1000, next_state))

            # Move
            next_state = state.forward()
            if next_state.pos in self.data:
                if next_state not in self.cost or cost + 1 < self.cost[next_state]:
                    self.cost[next_state] = cost + 1
                    heappush(pq, (cost + 1, next_state))
        return False

    def count_best(self):
        queue: collections.deque[State] = collections.deque()
        visited = set()
        for d in TURN_CCW:
            start_state = State(self.end, d)
            if start_state in self.cost and self.cost[start_state] == self.min_cost:
                queue.append(start_state)
                visited.add(start_state)

        cells = set()
        while queue:
            state = queue.popleft()
            dist = self.cost[state]
            cells.add(state.pos)

            # Backtracking turns:
            for prev_state in state.turn():
                if (
                    prev_state not in visited
                    and prev_state in self.cost
                    and self.cost[prev_state] + 1000 == dist
                ):
                    visited.add(prev_state)
                    queue.append(prev_state)

            # Backtracking moves:
            prev_state = state.back()
            if prev_state.pos in self.data:
                if (
                    prev_state not in visited
                    and prev_state in self.cost
                    and self.cost[prev_state] + 1 == dist
                ):
                    visited.add(prev_state)
                    queue.append(prev_state)

        return len(cells)


if __name__ == "__main__":
    lines = []

    for line in sys.stdin:
        lines.append(line.strip())

    grid = Grid(lines)
    if grid.solve():
        print(grid.min_cost)
        print(grid.count_best())
