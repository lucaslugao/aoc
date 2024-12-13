import sys
import re
import math
import dataclasses
from ortools.linear_solver import pywraplp


@dataclasses.dataclass(frozen=True)
class Machine:
    button_a: tuple[int, int]
    button_b: tuple[int, int]
    prize: tuple[int, int]

    def solve(self, problem):
        solver = pywraplp.Solver.CreateSolver("SCIP")
        a = solver.IntVar(0, 100 if problem == 1 else math.inf, "a")
        b = solver.IntVar(0, 100 if problem == 1 else math.inf, "b")
        solver.Minimize(3 * a + 1 * b)
        prize = self.prize
        if problem == 2:
            prize = (prize[0] + 10000000000000, prize[1] + 10000000000000)
        solver.Add(a * self.button_a[0] + b * self.button_b[0] == prize[0])
        solver.Add(a * self.button_a[1] + b * self.button_b[1] == prize[1])

        status = solver.Solve()

        if status == pywraplp.Solver.OPTIMAL:
            return int(solver.Objective().Value())
        else:
            return 0


if __name__ == "__main__":
    solution1 = 0
    solution2 = 0
    for line in sys.stdin:
        line = line.strip()
        if line.startswith("Button A"):
            match = re.match(r"Button A: X\+(\d+), Y\+(\d+)", line)
            a_x = int(match.group(1))
            a_y = int(match.group(2))
        elif line.startswith("Button B"):
            match = re.match(r"Button B: X\+(\d+), Y\+(\d+)", line)
            b_x = int(match.group(1))
            b_y = int(match.group(2))
        elif line.startswith("Prize"):
            match = re.match(r"Prize: X=(\d+), Y=(\d+)", line)
            prize_x = int(match.group(1))
            prize_y = int(match.group(2))
            m = Machine(
                (a_x, a_y),
                (b_x, b_y),
                (prize_x, prize_y),
            )
            solution1 += m.solve(1)
            solution2 += m.solve(2)
    print(solution1)
    print(solution2)
