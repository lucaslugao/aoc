import sys
import collections
import graphlib
from typing import List, Tuple


def parse(input_data: str) -> Tuple[List[Tuple[int, int]], List[List[int]]]:
    sections = input_data.strip().split("\n\n")
    rules_input = sections[0]
    updates_input = sections[1]

    rules: List[Tuple[int, int]] = []
    for rule in rules_input.splitlines():
        if rule.strip():
            x, y = map(int, rule.split("|"))
            rules.append((x, y))

    updates: List[List[int]] = []
    for update in updates_input.splitlines():
        if update.strip():
            updates.append(list(map(int, update.split(","))))

    return rules, updates


def is_valid(update: List[int], rules: List[Tuple[int, int]]) -> bool:
    position = {page: i for i, page in enumerate(update)}

    for x, y in rules:
        if x in position and y in position:
            if position[x] > position[y]:
                return False
    return True


def sub_rule(rules: List[Tuple[int, int]], update: List[int]) -> List[Tuple[int, int]]:
    upset = set(update)
    return [rule for rule in rules if rule[0] in upset and rule[1] in upset]


def valid_middle_sum(rules: List[Tuple[int, int]], updates: List[List[int]]) -> int:
    middle_sum = 0

    for update in updates:
        if is_valid(update, sub_rule(rules, update)):
            middle_sum += update[len(update) // 2]

    return middle_sum


def invalid_middle_sum(rules: List[Tuple[int, int]], updates: List[List[int]]) -> int:
    middle_sum = 0

    for update in updates:
        if not is_valid(update, rules):
            graph = collections.defaultdict(set)
            for x, y in sub_rule(rules, update):
                graph[x].add(y)

            ts = graphlib.TopologicalSorter(graph)
            topo_index = {v: i for i, v in enumerate(ts.static_order())}

            update.sort(key=lambda x: topo_index.get(x, float("inf")))
            middle_sum += update[len(update) // 2]

    return middle_sum


if __name__ == "__main__":
    input_data = sys.stdin.read()

    rules, updates = parse(input_data)

    solution1 = valid_middle_sum(rules, updates)
    solution2 = invalid_middle_sum(rules, updates)

    print(solution1)
    print(solution2)
