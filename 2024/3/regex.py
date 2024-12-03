import sys
import re

if __name__ == "__main__":
    mul_pattern = re.compile(r"mul\(((\d+),(\d+))\)")
    between_do_and_dont = re.compile(r"do\(\)(?:(?!don't\(\)).)*", re.DOTALL)
    data = "do()" + sys.stdin.read() + "don't()"

    def do_mul(data):
        return sum(
            sum(int(m.group(2)) * int(m.group(3)) for m in re.finditer(mul_pattern, d))
            for d in data
        )

    solution1 = do_mul([data])
    solution2 = do_mul(
        re.findall(
            between_do_and_dont,
            data,
        )
    )
    print(solution1)
    print(solution2)
