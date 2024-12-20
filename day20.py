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

SAMPLE = """###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""


def solve(input, max_cheat_len=20, limit=100):
    matrix = [ list(line) for line in input.splitlines() ]
    g = nx.grid_2d_graph(len(matrix), len(matrix[0]))
    for i, row in enumerate(matrix):
        for j, cell in enumerate(row):
            if cell == 'S':
                start = (i,j)
            elif cell == 'E':
                end = (i,j)
            elif cell == '#':
                g.remove_node((i,j))

    path = nx.shortest_path(g, start, end)
    path_nodes = { pos: n for n, pos in enumerate(path) }

    cheats = defaultdict(set)
    for start_index, (i1, j1) in enumerate(path):
        for di in range(-max_cheat_len, max_cheat_len + 1):
            i2 = i1 + di
            max_dj = max_cheat_len - abs(di)
            for dj in range(-max_dj, max_dj + 1):
                j2 = j1 + dj
                if (i2, j2) in path_nodes:
                    end_index = path_nodes[(i2, j2)]
                    if end_index > start_index:
                        cheat_len = abs(di) + abs(dj)
                        saved = end_index - start_index - cheat_len
                        if saved > 0:
                            cheats[saved].add((start_index, end_index))

    return sum(len(cheatset)
               for saved, cheatset in cheats.items()
               if saved >= limit)


def part1(input, limit = 100):
    return solve(input, max_cheat_len=2, limit=limit)


def part2(input, limit = 100):
    return solve(input, max_cheat_len=20, limit=limit)


def test_part1():
    assert part1(SAMPLE, 38) == 3


def test_part2():
    assert part2(SAMPLE, 74) == 7


if __name__ == '__main__':
    inputfile = re.sub(r"^.*?([^/]+)\.py$", r"\1.txt", __file__)
    INPUT = open(inputfile, "r").read()

    result = part1(INPUT)
    print("part1:", result)
    assert result == 1521

    result = part2(INPUT)
    print("part2:", result)
    assert result == 1013106

    num, total = timeit.Timer(lambda: part2(INPUT)).autorange()
    print("time=", total / num)
