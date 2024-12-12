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

def part1(input):
    matrix = input.splitlines()
    height = len(matrix)
    width = len(matrix[0])
    visited = set()
    regions = []
    result = 0
    for i, row in enumerate(matrix):
        for j, cell in enumerate(row):
            if (i,j) in visited:
                continue
            visited.add((i, j))
            region = set([(i, j)])
            edge = [(i, j)]
            perimeter = 0
            while len(edge) > 0:
                i1, j1 = edge.pop()
                for i2, j2 in neighbors(i1, j1):
                    if i2 < 0 or i2 >= height \
                       or j2 < 0 or j2 >= width:
                        perimeter += 1
                        continue
                    if (i2, j2) in region:
                        continue
                    cell2 = matrix[i2][j2]
                    if cell == cell2:
                        visited.add((i2, j2))
                        region.add((i2, j2))
                        edge.append((i2, j2))
                    else:
                        perimeter += 1
            result += len(region) * perimeter

    return result

def part2(input):
    matrix = input.splitlines()
    height = len(matrix)
    width = len(matrix[0])
    visited = set()
    regions = []
    result = 0
    for i, row in enumerate(matrix):
        for j, cell in enumerate(row):
            if (i,j) in visited:
                continue
            visited.add((i, j))
            region = set([(i, j)])
            frontier = [(i, j)]
            edges = []
            perimeter = 0
            while len(frontier) > 0:
                i1, j1 = frontier.pop()
                for d, (i2, j2) in enumerate(neighbors(i1, j1)):
                    if i2 < 0 or i2 >= height \
                       or j2 < 0 or j2 >= width:
                        edges.append((d, (i1, j1)))
                        perimeter += 1
                        continue
                    if (i2, j2) in region:
                        continue
                    cell2 = matrix[i2][j2]
                    if cell == cell2:
                        visited.add((i2, j2))
                        region.add((i2, j2))
                        frontier.append((i2, j2))
                    else:
                        edges.append((d, (i1, j1)))
                        perimeter += 1
            edgecount = 0
            print(edges)
            for d, (i1, j1) in edges:
                i2, j2 = (i1, j1 - 1) if d in [0, 3] else (i1 - 1, j1)
                print(f"looking at {(i2, j2)} from {(d, (i1, j1))}")
                if i2 < 0 or i2 >= height \
                   or j2 < 0 or j2 >= width:
                    print("outside")
                    edgecount += 1
                    continue
                if (d, (i2, j2)) in edges:
                    print("skipping", (d, (i2, j2)), "from", (d, (i1, j1)))
                    continue
                edgecount += 1
            print(edgecount)

            result += len(region) * edgecount
            regions.append(region)

    return result

if __name__ == '__main__':
    INPUT = open("day12.txt", "r").read()

    result = part1(INPUT)
    print("part1:", result)
    assert result == 1387004

    result = part2(INPUT)
    print("part2:", result)
    #assert result == 224577979481346

    #num, total = timeit.Timer(lambda: part2(INPUT)).autorange()
    #print("time=", total / num)
