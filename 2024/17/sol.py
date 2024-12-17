import sys
import dataclasses
from typing import Tuple, List
from enum import Enum


class Opcode(Enum):
    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7


@dataclasses.dataclass
class Machine:
    A: int
    B: int
    C: int
    program: Tuple[int]

    def __init__(self, lines):
        self.A = int(lines[0].split(":")[1].strip())
        self.B = int(lines[1].split(":")[1].strip())
        self.C = int(lines[2].split(":")[1].strip())
        self.program = tuple(map(int, lines[4].split(":")[1].strip().split(",")))

    def __str__(self):
        return f"A: {self.A}, B: {self.B}, C: {self.C} Program: {self.program}"

    def combo(self, operand, A, B, C):
        if operand <= 3:
            return operand
        elif operand == 4:
            return A
        elif operand == 5:
            return B
        elif operand == 6:
            return C
        return -1

    def run(self):
        ip = 0
        output = []
        A, B, C = self.A, self.B, self.C

        while ip < len(self.program):
            opcode = Opcode(self.program[ip])
            if ip + 1 >= len(self.program):
                break
            literal = self.program[ip + 1]
            combo = self.combo(literal, A, B, C)
            if opcode == Opcode.ADV:
                A >>= combo
            elif opcode == Opcode.BXL:
                B ^= literal
            elif opcode == Opcode.BST:
                B = combo & 7
            elif opcode == Opcode.JNZ:
                if A != 0:
                    ip = literal
                    continue
            elif opcode == Opcode.BXC:
                B ^= C
            elif opcode == Opcode.OUT:
                output.append(combo & 7)
            elif opcode == Opcode.BDV:
                B = A >> combo
            elif opcode == Opcode.CDV:
                C = A >> combo
            ip += 2
        return output


def oct_to_dec(x):
    return sum(d * 8**i for i, d in enumerate(reversed(x)))


def count_matching_suffix(A, B):
    count = 0
    for a, b in zip(reversed(A), reversed(B)):
        if a == b:
            count += 1
        else:
            break
    return count


@dataclasses.dataclass
class Candidate:
    score: int = 0
    deci: int = 0
    octo: List[int] = dataclasses.field(default_factory=list)
    run: List[int] = dataclasses.field(default_factory=list)


if __name__ == "__main__":
    lines = sys.stdin.readlines()
    machine = Machine(lines)
    print(",".join(map(str, machine.run())))

    # Genetic inspired algorithm to find the smallest quine input
    population = [Candidate()]
    for i in range(len(machine.program)):
        new_population = []
        for c in population:
            for e in range(1 << 3):
                nA = c.octo + [e]
                machine.A = oct_to_dec(nA)
                run = machine.run()
                score = count_matching_suffix(run, machine.program)
                new_population.append(Candidate(score, oct_to_dec(nA), nA, run))
        highscore = max(new_population, key=lambda x: x.score)
        population = [p for p in new_population if p.score == highscore.score]
    print(min(population, key=lambda x: x.deci).deci)
