import sys

if __name__ == "__main__":
    numbers = [[int(t) for t in line.split()] for line in sys.stdin]

    def valid1(row):
        diff = [row[i] - row[i - 1] for i in range(1, len(row))]
        return all(1 <= abs(d) <= 3 and d * diff[0] > 0 for d in diff)

    def valid2(row):
        return any(valid1(row[:i] + row[i + 1 :]) for i in range(len(row)))

    solution1 = sum(valid1(row) for row in numbers)
    print(solution1)

    solution2 = sum(valid2(row) for row in numbers)
    print(solution2)
