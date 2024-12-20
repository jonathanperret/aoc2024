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
    walls = { (i,j)
             for i, row in enumerate(matrix)
             for j, cell in enumerate(row)
             if cell == '#' }
    for i, row in enumerate(matrix):
        for j, cell in enumerate(row):
            if cell == 'S':
                start = (i,j)
            elif cell == 'E':
                end = (i,j)

    g = nx.grid_2d_graph(len(matrix), len(matrix[0]))
    print(g)
    for (i,j) in walls:
        g.remove_node((i,j))
    print(g)

    max_len = nx.shortest_path_length(g, start, end)
    print("non-cheating:", max_len)


    paths_from_start = nx.single_source_shortest_path_length(g, start)
    # print(f"paths_from_start: {paths_from_start}")
    paths_to_end = nx.single_source_shortest_path_length(g, end)
    # print(f"paths_to_end: {paths_to_end}")

    cheats = defaultdict(set)
    for i, row in enumerate(matrix):
        for j, cell in enumerate(row):
            if cell != '#':
                for di in range(max_cheat_len + 1):
                    for dj in range(max_cheat_len + 1 - di):
                        try:
                            new_cell = matrix[i+di][j+dj]
                        except IndexError:
                            continue
                        if new_cell != '#':
                            new_pos = (i+di, j+dj)

                            to_cell = paths_from_start[(i,j)]
                            rest = paths_to_end[new_pos]
                            total = to_cell + di + dj + rest
                            saved = max_len - total
                            if saved > 0:
                                cheats[saved].add(((i,j), new_pos))

                            to_cell = paths_from_start[new_pos]
                            rest = paths_to_end[(i,j)]
                            total = to_cell + di + dj + rest
                            saved = max_len - total
                            if saved > 0:
                                cheats[saved].add(((i,j), new_pos))



    result = 0
    for saved in sorted(cheats.keys()):
        print(saved, len(cheats[saved]))
        if saved >= limit:
            result += len(cheats[saved])

    return result


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
    # 266594 too low
    # 558948 too low
    #assert result == 724388733465031

    #num, total = timeit.Timer(lambda: part2(INPUT)).autorange()
    #print("time=", total / num)
