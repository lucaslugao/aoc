import sys
import functools


@functools.cache
def count_ways(design, patterns, i=0):
    if i == len(design):
        return 1
    total_ways = 0
    for pattern in patterns:
        if design.startswith(pattern, i):
            total_ways += count_ways(design, patterns, i + len(pattern))
    return total_ways


if __name__ == "__main__":
    lines = [line.strip() for line in sys.stdin]

    patterns_line = lines[0].strip()
    patterns = tuple(patterns_line.split(", "))

    designs = [line.strip() for line in lines[2:] if line.strip()]

    res1 = 0
    res2 = 0

    for design in designs:
        ways = count_ways(design, patterns)
        res1 += 1 if ways > 0 else 0
        res2 += ways

    print(res1)
    print(res2)
