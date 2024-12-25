import sys
import dataclasses
import functools
from typing import Literal, Dict, FrozenSet
import networkx as nx


@dataclasses.dataclass(frozen=True)
class Relation:
    vars: FrozenSet[str]
    op: Literal["AND", "OR", "XOR"]

    @staticmethod
    def Create(left, right, op):
        return Relation(frozenset([left, right]), op)


def solve1(vars: Dict[str, int | Relation]):
    @functools.cache
    def evaluate(target):
        if isinstance(vars[target], int):
            return vars[target]
        else:
            rel = vars[target]
            left, right = rel.vars
            lval, rval = evaluate(left), evaluate(right)
            if rel.op == "AND":
                return lval & rval
            elif rel.op == "OR":
                return lval | rval
            elif rel.op == "XOR":
                return lval ^ rval
            else:
                raise ValueError(f"Unknown operator {rel.op}")

    z_targets = [k for k in vars if k.startswith("z")]
    z_targets.sort(key=lambda x: -int(x[1:]))

    number = "".join(str(evaluate(k)) for k in z_targets)
    return int(number, 2)


def solve2(vars: Dict[str, int | Relation]):
    def has_invalid_and_connection(target, rel):
        return (
            rel.op == "AND"
            and "x00" not in rel.vars
            and any(
                target in other.vars and other.op != "OR"
                for other in vars.values()
                if isinstance(other, Relation)
            )
        )

    def has_invalid_xor_connection(target, rel):
        return rel.op == "XOR" and all(
            not x.startswith(("x", "y", "z")) for x in rel.vars | {target}
        )

    def has_invalid_xor_with_or(target, rel):
        return rel.op == "XOR" and any(
            target in other.vars and other.op == "OR"
            for other in vars.values()
            if isinstance(other, Relation)
        )

    def is_invalid_z_target(target, rel):
        return target.startswith("z") and rel.op != "XOR" and target != "z45"

    wrong = []
    for target, rel in vars.items():
        if isinstance(rel, Relation):
            if (
                has_invalid_and_connection(target, rel)
                or has_invalid_xor_connection(target, rel)
                or has_invalid_xor_with_or(target, rel)
                or is_invalid_z_target(target, rel)
            ):
                wrong.append(target)

    return ",".join(sorted(wrong))


if __name__ == "__main__":
    sections = sys.stdin.read().split("\n\n")
    init_s = sections[0].split("\n")
    rels_s = sections[1].split("\n")

    vars: Dict[str, int | Relation] = dict()

    for line in init_s:
        target, value = line.split(":")
        vars[target] = int(value.strip())

    to_evaluate = set()
    for line in rels_s:
        predicate, target = line.split("->")
        left, op, right = predicate.split()
        target = target.strip()
        vars[target] = Relation.Create(left, right, op)
        to_evaluate.add(target)

    print(solve1(vars))
    print(solve2(vars))
