from itertools import *
from more_itertools import *
import re
from functools import partial, cmp_to_key

SAMPLE = """190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

def parse(input):
    lines = input.splitlines()
    return [ list(map(int, re.split(':? ', line))) for line in lines ]

def solve(input, allow_concat):
    equations = parse(input)

    def check(target, nums):
        if len(nums) == 1:
            return nums[0] == target

        *nums, lastnum = nums

        if target < lastnum:
            return False

        # +
        if check(target - lastnum, nums):
            return True

        # *
        q, r = divmod(target, lastnum)
        if r == 0 and check(q, nums):
            return True

        # ||
        if allow_concat and target != lastnum:
            left = int(str(target).removesuffix(str(lastnum)))
            if left < target and check(left, nums):
                return True

        return False

    return sum(target
               for target, *nums in equations
               if check(target, nums))

def part1(input):
    return solve(input, allow_concat=False)

def part2(input):
    return solve(input, allow_concat=True)

INPUT = open("day7.txt", "r").read()

result = part1(SAMPLE)
print("part1:", result)
assert result == 3749

result = part1(INPUT)
print("part1:", result)
assert result == 4122618559853

result = part2(SAMPLE)
print("part2:", result)
assert result == 11387

result = part2(INPUT)
print("part2:", result)
assert result == 227615740238334
