import sys


def is_solvable(target, nums, concat=False):
    if len(nums) == 1:
        return target == nums[0]
    if target >= nums[-1] and is_solvable(target - nums[-1], nums[:-1], concat):
        return True
    if target % nums[-1] == 0 and is_solvable(target // nums[-1], nums[:-1], concat):
        return True
    if concat:
        factor = 10 ** len(str(nums[-1]))
        if target >= factor and target % factor == nums[-1]:
            if is_solvable(target // factor, nums[:-1], concat):
                return True
    return False


if __name__ == "__main__":
    solution1 = 0
    solution2 = 0
    for line in sys.stdin:
        targetstr, numsstr = line.strip().split(":")
        target = int(targetstr)
        nums = [int(x.strip()) for x in numsstr.strip().split(" ")]
        if is_solvable(target, nums):
            solution1 += target
        if is_solvable(target, nums, True):
            solution2 += target
    print(solution1)
    print(solution2)
