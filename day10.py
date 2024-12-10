from itertools import *
from more_itertools import *
import re
from functools import partial, cmp_to_key
from collections import defaultdict
from math import gcd
from heapq import *
import timeit

SAMPLE = """89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""

def neighbors(i, j):
    return [(i-1, j),
            (i  , j-1), (i  , j+1),
            (i+1, j)]

def score(matrix, startpos):
    visited = set([startpos])
    edge = [ startpos ]
    (start_i, start_j) = startpos
    height = len(matrix)
    width = len(matrix[0])
    result = 0
    while len(edge) > 0:
        pos = edge.pop()
        i, j = pos
        for next_i, next_j in neighbors(*pos):
            if next_i >= 0 and next_i < height and next_j >= 0 and next_j < width \
               and (next_i, next_j) not in visited \
               and matrix[next_i][next_j] == matrix[i][j] + 1:
                visited.add((next_i, next_j))
                if matrix[next_i][next_j] == 9:
                    result += 1
                else:
                    edge.append((next_i, next_j))
    return result

def rate(matrix, startpos):
    visited = set([startpos])
    edge = [ startpos ]
    (start_i, start_j) = startpos
    height = len(matrix)
    width = len(matrix[0])
    result = 0
    paths = defaultdict(lambda: 0)
    while len(edge) > 0:
        pos = edge.pop()
        i, j = pos
        for next_i, next_j in neighbors(*pos):
            if next_i >= 0 and next_i < height and next_j >= 0 and next_j < width \
               and matrix[next_i][next_j] == matrix[i][j] + 1:
                if matrix[next_i][next_j] == 9:
                    result += 1
                else:
                    edge.append((next_i, next_j))
    return result


def part1(input):
    matrix = [ list(map(int, line)) for line in input.splitlines() ]
    result = 0
    for i, row in enumerate(matrix):
        for j, cell in enumerate(row):
            if cell == 0:
                result += score(matrix, (i, j))
    return result

def part2(input):
    matrix = [ list(map(int, line)) for line in input.splitlines() ]
    result = 0
    for i, row in enumerate(matrix):
        for j, cell in enumerate(row):
            if cell == 0:
                result += rate(matrix, (i, j))
    return result

if __name__ == '__main__':
    INPUT = open("day10.txt", "r").read()

    result = part1(INPUT)
    print("part1:", result)
    assert result == 776

    result = part2(INPUT)
    print("part2:", result)
    assert result == 1657

    #num, total = timeit.Timer(lambda: part2(INPUT)).autorange()
    #print("time=", total / num)
