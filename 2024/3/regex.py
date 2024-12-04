import sys
import re

if __name__ == "__main__":
    mul_do_dont = re.compile(r"mul\((\d+),(\d+)\)|do\(\)|don't\(\)")
    data = sys.stdin.read()

    solution1 = 0
    solution2 = 0
    do = True
    for m in re.finditer(mul_do_dont, data):
        if m.group(0) == "do()":
            do = True
        elif m.group(0) == "don't()":
            do = False
        else:
            v = int(m.group(1)) * int(m.group(2))
            solution1 += v
            if do:
                solution2 += v
    print(solution1)
    print(solution2)
