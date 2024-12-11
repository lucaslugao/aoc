import sys
import functools


@functools.cache
def count(stone: str, blinks: int) -> int:
    if blinks == 0:
        return 1

    return sum(count(ns, blinks - 1) for ns in transform(stone))


@functools.cache
def transform(stone: int) -> list[int]:
    if stone == 0:
        return [1]

    sstone = str(stone)
    length = len(sstone)
    if length % 2 == 0:
        mid = length // 2
        left_part = sstone[:mid]
        right_part = sstone[mid:]

        return [int(left_part), int(right_part)]

    return [stone * 2024]


if __name__ == "__main__":
    line = sys.stdin.readline().strip()
    stones = [int(x) for x in line.split()]

    solution1 = 0
    solution2 = 0
    for s in stones:
        solution1 += count(s, 25)
        solution2 += count(s, 75)
    print(solution1)
    print(solution2)
