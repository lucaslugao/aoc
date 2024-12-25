import sys
import itertools


if __name__ == "__main__":
    objs = [o.split("\n") for o in sys.stdin.read().split("\n\n")]

    locks = []
    keys = []
    for obj in objs:
        is_lock = all(c == "#" for c in obj[0])
        profile = [
            sum(1 for line in obj if line[i] == "#") - 1 for i in range(len(obj[0]))
        ]
        if is_lock:
            locks.append(profile)
        else:
            keys.append(profile)

    total = 0
    for lock, key in itertools.product(locks, keys):
        add = [o + k for o, k in zip(lock, key)]
        if all(a <= 5 for a in add):
            total += 1
    print(total)
