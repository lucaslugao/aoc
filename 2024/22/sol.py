import sys
import collections

MOD = 16777216


def next_secret(n):
    s = (n * 64) % MOD
    n = (n ^ s) % MOD

    s = n >> 5
    n = (n ^ s) % MOD

    s = (n * 2048) % MOD
    n = (n ^ s) % MOD

    return n


if __name__ == "__main__":
    lines = [line.strip() for line in sys.stdin if line.strip()]
    total_price_at_pattern = collections.defaultdict(int)
    total = 0

    for line in lines:
        n = int(line)

        price_at_first = {}
        prev_price = n % 10

        diffs = collections.deque(maxlen=4)

        for _ in range(2000):
            new_n = next_secret(n)
            curr_price = new_n % 10
            diff = curr_price - prev_price
            diffs.append(diff)

            if len(diffs) == 4:
                pattern = tuple(diffs)
                if pattern not in price_at_first:
                    price_at_first[pattern] = curr_price

            prev_price = curr_price
            n = new_n
        total += n

        for pattern, price in price_at_first.items():
            total_price_at_pattern[pattern] += price

    print(total)
    print(max(total_price_at_pattern.values()))
