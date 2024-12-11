from itertools import *
from more_itertools import *
import re
from functools import partial, cmp_to_key
from collections import defaultdict
from math import gcd
from heapq import *
import timeit
import functools

SAMPLE = """125 17
"""

@functools.cache
def expand(s, times):
    if times == 0:
        return 1

    if s == 0:
        return expand(1, times - 1)

    ss = str(s)
    if len(ss) % 2 == 0:
        s1, s2 = ss[:len(ss)//2], ss[len(ss)//2:]
        return expand(int(s1), times - 1) + expand(int(s2), times - 1)

    return expand(s * 2024, times -1)

def solve(input, times):
    stones = list(map(int, input.split()))
    return sum(expand(s, times) for s in stones)

def part1(input):
    return solve(input, 25)

def part2(input):
    return solve(input, 75)

if __name__ == '__main__':
    INPUT = open("day11.txt", "r").read()

    result = part1(INPUT)
    print("part1:", result)
    assert result == 189547

    result = part2(INPUT)
    print("part2:", result)
    assert result == 224577979481346

    num, total = timeit.Timer(lambda: part2(INPUT)).autorange()
    print("time=", total / num)
