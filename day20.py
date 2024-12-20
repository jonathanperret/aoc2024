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


def part1(input, limit=100):
    matrix = [ list(line) for line in input.splitlines() ]
    walls = { (i,j)
             for i, row in enumerate(matrix)
             for j, cell in enumerate(row)
             if matrix[i][j] == '#' }
    for i, row in enumerate(matrix):
        for j, cell in enumerate(row):
            if matrix[i][j] == 'S':
                start = (i,j)
            elif matrix[i][j] == 'E':
                end = (i,j)

    g = nx.grid_2d_graph(len(matrix), len(matrix[0]))
    print(g)
    for (i,j) in walls:
        g.remove_node((i,j))
    print(g)

    max_len = nx.shortest_path_length(g, start, end)
    print("non-cheating:", max_len)

    cheats = defaultdict(set)
    for i, row in enumerate(matrix):
        for j, cell in enumerate(row):
            if cell != '#':
                for new_pos in [(i+2,j), (i,j+2)]:
                    try:
                        new_cell = matrix[new_pos[0]][new_pos[1]]
                    except IndexError:
                        continue
                    if new_cell != '#':
                        g.add_edge((i,j), new_pos)
                        min_len = nx.shortest_path_length(g, start, end)
                        saved = max_len-min_len-1
                        cheats[saved].add(((i,j), new_pos))
                        print(i, j, saved)
                        g.remove_edge((i,j), new_pos)

    result = 0
    for saved in sorted(cheats.keys()):
        print(saved, len(cheats[saved]))
        if saved >= limit:
            result += len(cheats[saved])

    return result


def part2(input):
    return 2


def test_part1():
    assert part1(SAMPLE, 38) == 3


def test_part2():
    assert part2(SAMPLE) == 2


if __name__ == '__main__':
    inputfile = re.sub(r"^.*?([^/]+)\.py$", r"\1.txt", __file__)
    INPUT = open(inputfile, "r").read()

    result = part1(INPUT)
    print("part1:", result)
    assert result == 1521

    #result = part2(INPUT)
    #print("part2:", result)
    #assert result == 724388733465031

    #num, total = timeit.Timer(lambda: part2(INPUT)).autorange()
    #print("time=", total / num)
