from itertools import *
from more_itertools import *
import re
from functools import partial, cmp_to_key
from collections import defaultdict
from math import gcd, sqrt
from heapq import *
import timeit
import functools
import networkx as nx

SAMPLE = """1
10
100
2024
"""

def make_secret(secret, rounds):
    for _ in range(rounds):
        secret = ((secret << 6) ^ secret) & 0xffffff
        secret = ((secret >> 5) ^ secret)
        secret = ((secret << 11) ^ secret) & 0xffffff
    return secret


def part1(input):
    seeds = map(int, input.splitlines())
    result = 0
    for seed in seeds:
        secret = make_secret(seed, 2000)
        result += secret
    return result


def part2(input):
    return 2


def test_part1():
    assert part1(SAMPLE) == 37327623


def test_part2():
    assert part2(SAMPLE) == 2


if __name__ == '__main__':
    inputfile = re.sub(r"^.*?([^/]+)\.py$", r"\1.txt", __file__)
    INPUT = open(inputfile, "r").read()

    result = part1(INPUT)
    print("part1:", result)
    assert result == 13753970725

    # result = part2(INPUT)
    # print("part2:", result)
    # assert result == 170279148659464

    # num, total = timeit.Timer(lambda: part2(INPUT)).autorange()
    # print("time=", total / num)
