from itertools import *
from more_itertools import *
import re
from functools import partial, cmp_to_key
from collections import defaultdict
from math import gcd
from heapq import *
import timeit
import functools

SAMPLE = """RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE
"""

def neighbors(i, j):
    return [(i-1, j), (i, j-1), (i, j+1), (i+1, j)]


def flood(matrix, start):
    height = len(matrix)
    width = len(matrix[0])
    region = {start}
    edges = set()
    i, j = start
    cell = matrix[i][j]
    frontier = [start]
    while len(frontier) > 0:
        i1, j1 = frontier.pop()
        for d, (i2, j2) in enumerate(neighbors(i1, j1)):
            if (i2, j2) in region:
                continue
            if i2 >= 0 and i2 < height \
               and j2 >= 0 and j2 < width \
               and matrix[i2][j2] == cell:
                region.add((i2, j2))
                frontier.append((i2, j2))
            else:
                edges.add((d, (i1, j1)))
    return region, edges


def find_regions(input):
    matrix = input.splitlines()
    visited = set()
    result = 0
    regions = []
    for i, j in product(range(len(matrix)), range(len(matrix[0]))):
        if (i,j) in visited:
            continue
        region, edges = flood(matrix, (i, j))
        regions.append((region, edges))
        visited |= region
    return regions


def part1(input):
    return sum(len(region) * len(edges)
               for region, edges in find_regions(input))


def part2(input):
    result = 0
    for region, edges in find_regions(input):
        edgecount = 0
        for d, (i1, j1) in edges:
            i2, j2 = (i1, j1 - 1) if d in [0, 3] else (i1 - 1, j1)
            if (d, (i2, j2)) not in edges:
                edgecount += 1

        result += len(region) * edgecount

    return result

def test_part1():
    assert part1(SAMPLE) == 1930

def test_part2():
    assert part2(SAMPLE) == 1206

if __name__ == '__main__':
    INPUT = open("day12.txt", "r").read()

    result = part1(INPUT)
    print("part1:", result)
    assert result == 1387004

    result = part2(INPUT)
    print("part2:", result)
    assert result == 844198

    num, total = timeit.Timer(lambda: part2(INPUT)).autorange()
    print("time=", total / num)
