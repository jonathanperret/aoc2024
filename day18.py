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

SAMPLE = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""

def part1(input, size = 71, limit=1024):
    walls = [ tuple(map(int, line.split(',')))
              for line in input.splitlines()[:limit] ]

    g = nx.grid_2d_graph(size, size)

    for (i,j) in walls:
        g.remove_node((i,j))

    return nx.shortest_path_length(g, (0,0), (size-1,size-1))


def part2(input, size = 71, limit = 1024):
    walls = [ tuple(map(int, line.split(',')))
              for line in input.splitlines() ]

    g = nx.grid_2d_graph(size, size)

    path = None
    for i,j in walls:
        if g.has_node((i,j)):
            g.remove_node((i,j))

        if path is None or (i,j) in path:
            try:
                path = set(nx.shortest_path(g, (0, 0), (size-1, size-1)))
            except:
                return f"{i},{j}"
            # print((i,j))
            # print('\n'.join(''.join(['O' if (i,j) in path
            #                          else '.' if g.has_node((i,j))
            #                          else '#'
            #                          for j in range(size)]) for i in range(size)))

    return None


def test_part1():
    assert part1(SAMPLE, 7, 12) == 22


def test_part2():
    assert part2(SAMPLE, 7, 12) == '6,1'


if __name__ == '__main__':
    inputfile = re.sub(r"^.*?([^/]+)\.py$", r"\1.txt", __file__)
    INPUT = open(inputfile, "r").read()

    result = part1(INPUT)
    print("part1:", result)
    assert result == 290

    result = part2(INPUT)
    print("part2:", result)
    assert result == '64,54'

    num, total = timeit.Timer(lambda: part2(INPUT)).autorange()
    print("time=", total / num)
