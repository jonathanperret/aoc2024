from itertools import *
from more_itertools import *
import re
from functools import partial, cmp_to_key
from collections import defaultdict, Counter
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

SAMPLE2 = """1
2
3
2024
"""

def xorshift(secret):
    secret = ((secret << 6) ^ secret) & 0xffffff
    secret = ((secret >> 5) ^ secret) & 0xffffff
    secret = ((secret << 11) ^ secret) & 0xffffff
    return secret


def make_secret(secret, rounds):
    for _ in range(rounds):
        secret = xorshift(secret)
    return secret


def part1(input):
    secrets = map(int, input.splitlines())
    result = 0
    for secret in secrets:
        secret = make_secret(secret, 2000)
        result += secret
    return result


def part2(input):
    secrets = map(int, input.splitlines())

    seqgross = Counter()
    for monkey, secret in enumerate(secrets):
        price = secret % 10
        seq = 0
        seen = set()
        mask = 19 ** 4
        for i in range(2000):
            secret = xorshift(secret)
            old, price = price, secret % 10
            seq = (seq * 19 + (9 + price - old)) % mask
            if i >= 4 and seq not in seen:
                seen.add(seq)
                seqgross[seq] += price

    return max(seqgross.values())


def test_part1():
    assert part1(SAMPLE) == 37327623


def test_part2():
    assert part2(SAMPLE2) == 23


if __name__ == '__main__':
    inputfile = re.sub(r"^.*?([^/]+)\.py$", r"\1.txt", __file__)
    INPUT = open(inputfile, "r").read()

    result = part1(INPUT)
    print("part1:", result)
    assert result == 13753970725

    result = part2(INPUT)
    print("part2:", result)
    assert result == 1570

    num, total = timeit.Timer(lambda: part2(INPUT)).autorange()
    print("time=", total / num)
