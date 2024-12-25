import dataclasses
from typing import Dict
import itertools


@dataclasses.dataclass(frozen=True)
class State:
    layer: int
    from_key: str
    to_key: str


def build_coords(rows):
    return {char: (x, y) for y, row in enumerate(rows) for x, char in enumerate(row)}


ARROWS = build_coords([" ^A", "<v>"])
KEYPAD = build_coords(["789", "456", "123", " 0A"])


def solve(code, robots):
    cost: Dict[State, int] = {}
    for from_key, to_key in itertools.product(ARROWS, ARROWS):
        cost[State(0, from_key, to_key)] = 1

    def program_cost(layer, program):
        pos = "A"
        res = 0
        for key in program:
            res += cost[State(layer, pos, key)]
            pos = key
        return res

    for layer in range(1, robots + 2):
        coords = KEYPAD if layer == robots + 1 else ARROWS

        for from_key, to_key in itertools.product(coords, coords):
            (xf, yf) = coords[from_key]
            (xt, yt) = coords[to_key]

            h_moves = (">" if xt > xf else "<") * abs(xt - xf)
            v_moves = ("^" if yt < yf else "v") * abs(yt - yf)

            candidates = []

            if (xt, yf) != coords[" "]:
                candidates.append(h_moves + v_moves + "A")
            if (xf, yt) != coords[" "]:
                candidates.append(v_moves + h_moves + "A")

            if not candidates:
                continue

            cost[State(layer, from_key, to_key)] = min(
                program_cost(layer - 1, candidate) for candidate in candidates
            )

    return program_cost(robots + 1, code)


def complexity(code, sol):
    return sol * int(code[:-1])


if __name__ == "__main__":
    import sys

    codes = [line.strip() for line in sys.stdin]

    res1 = 0
    res2 = 0
    for code in codes:
        res1 += complexity(code, solve(code, 2))
        res2 += complexity(code, solve(code, 25))

    print(res1)
    print(res2)
