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

def part1(input):
    lines = input.splitlines()
    equations = [ list(map(int, re.split(':? ', line))) for line in lines ]
    result = 0
    for equation in equations:
        print(equation)
        for bits in range(2 ** (len(equation) - 2)):
            target, total, *nums = equation
            for bit, num in enumerate(nums):
                if bits & (1 << bit):
                    total += num
                else:
                    total *= num
            if total == target:
                result += target
                break
    return result

def part2(input):
    lines = input.splitlines()
    equations = [ list(map(int, re.split(':? ', line))) for line in lines ]
    result = 0
    for equation in equations:
        print(equation)
        for bits in range(3 ** (len(equation) - 2)):
            target, total, *nums = equation
            rest = bits
            # print("trying", bits)
            for num in nums:
                rest, op = divmod(rest, 3)
                if op == 0:
                    total += num
                if op == 1:
                    total *= num
                elif op == 2:
                    #print(f"{total} || {num} -> {int(str(total) + str(num))}")
                    total = int(str(total) + str(num))
            if total == target:
                print("ok")
                result += target
                break
    return result

INPUT = open("day7.txt", "r").read()

# print("part1:", part1(SAMPLE))
# print("part1:", part1(INPUT))
print("part2:", part2(SAMPLE))
print("part2:", part2(INPUT))
