import sys
import collections

if __name__ == "__main__":
    # Read input line by line from standard input
    numbers = [[int(t) for t in line.split()] for line in sys.stdin]
    # Build the two sorted lists from each column
    list1, list2 = [sorted([r[c] for r in numbers]) for c in range(2)]

    # First solution is the sum of the pairwise absolute difference
    solution1 = sum(abs(n1 - n2) for n1, n2 in zip(list1, list2))
    print(solution1)

    # Count the number of times each element appears in the second list
    counter2 = collections.Counter(list2)
    # Second solution is the sum of the product of the number in the first list
    # by its appearance in the second list
    solution2 = sum(n1 * counter2[n1] for n1 in list1)
    print(solution2)
