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

SAMPLE = """r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""

def parse(input):
    towels, designs = input.split("\n\n")
    towels = towels.split(", ")
    designs = designs.splitlines()
    return (towels, designs)


def part1(input):
    towels, designs = parse(input)

    @functools.cache
    def make(design):
        if len(design) == 0:
            return True
        return any(make(design[len(towel):])
                   for towel in towels
                   if design.startswith(towel))

    return sum(map(make, designs))


def part2(input):
    towels, designs = parse(input)

    @functools.cache
    def make(design):
        if len(design) == 0:
            return 1
        return sum(make(design[len(towel):])
                   for towel in towels
                   if design.startswith(towel))

    return sum(map(make, designs))


def test_part1():
    assert part1(SAMPLE) == 6


def test_part2():
    assert part2(SAMPLE) == 16


if __name__ == '__main__':
    inputfile = re.sub(r"^.*?([^/]+)\.py$", r"\1.txt", __file__)
    INPUT = open(inputfile, "r").read()

    result = part1(INPUT)
    print("part1:", result)
    assert result == 367

    result = part2(INPUT)
    print("part2:", result)
    assert result == 724388733465031

    num, total = timeit.Timer(lambda: part2(INPUT)).autorange()
    print("time=", total / num)
