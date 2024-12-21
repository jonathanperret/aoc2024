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

SAMPLE = """029A
980A
179A
456A
379A
"""

def make_numpad():
    g = nx.DiGraph()
    g.add_edge('7', '8', direction='>')
    g.add_edge('8', '7', direction='<')
    g.add_edge('8', '9', direction='>')
    g.add_edge('9', '8', direction='<')

    g.add_edge('4', '5', direction='>')
    g.add_edge('5', '4', direction='<')
    g.add_edge('5', '6', direction='>')
    g.add_edge('6', '5', direction='<')

    g.add_edge('1', '2', direction='>')
    g.add_edge('2', '1', direction='<')
    g.add_edge('2', '3', direction='>')
    g.add_edge('3', '2', direction='<')

    g.add_edge('0', 'A', direction='>')
    g.add_edge('A', '0', direction='<')

    g.add_edge('7', '4', direction='v')
    g.add_edge('4', '7', direction='^')
    g.add_edge('4', '1', direction='v')
    g.add_edge('1', '4', direction='^')

    g.add_edge('8', '5', direction='v')
    g.add_edge('5', '8', direction='^')
    g.add_edge('5', '2', direction='v')
    g.add_edge('2', '5', direction='^')
    g.add_edge('2', '0', direction='v')
    g.add_edge('0', '2', direction='^')

    g.add_edge('9', '6', direction='v')
    g.add_edge('6', '9', direction='^')
    g.add_edge('6', '3', direction='v')
    g.add_edge('3', '6', direction='^')
    g.add_edge('3', 'A', direction='v')
    g.add_edge('A', '3', direction='^')

    return g


def make_dirpad():
    g = nx.DiGraph()

    g.add_edge('^', 'A', direction='>')
    g.add_edge('A', '^', direction='<')

    g.add_edge('<', 'v', direction='>')
    g.add_edge('v', '<', direction='<')
    g.add_edge('v', '>', direction='>')
    g.add_edge('>', 'v', direction='<')

    g.add_edge('^', 'v', direction='v')
    g.add_edge('v', '^', direction='^')

    g.add_edge('A', '>', direction='v')
    g.add_edge('>', 'A', direction='^')

    return g


numpad = make_numpad()
dirpad = make_dirpad()


def pad_paths(pad, previous_key, key):
    if key == previous_key:
        return [['A']]

    paths = nx.all_shortest_paths(pad, source=previous_key, target=key)
    return [
        [pad.get_edge_data(old, new)['direction']
         for old, new in pairwise(path)] + ['A']
        for path in paths
    ]


def numpad_paths(previous_key, key):
    return pad_paths(numpad, previous_key, key)


def dirpad_paths(previous_key, key):
    return pad_paths(dirpad, previous_key, key)


def all_num_paths(code):
    result = [[]]
    for old, new in pairwise(['A'] + list(code)):
        paths = numpad_paths(old, new)
        result = [ r + p
                   for r in result
                   for p in paths ]
    return result


@functools.cache
def min_dirpad_length(old, new, n):
    return min(len(dirs) if n == 0
               else min_dirN_path_length(dirs, n-1)
               for dirs in dirpad_paths(old, new))


def min_dirN_path_length(dirs, n):
    return sum(min_dirpad_length(old, new, n)
               for old, new in pairwise(['A'] + dirs))


def shortest_path_length(code, depth):
    return min(min_dirN_path_length(dirs, depth-1)
               for dirs in all_num_paths(code))


def solve(code, depth):
    return shortest_path_length(code, depth) * int(code[:-1])


def part1(input):
    return sum(solve(code, 2)
               for code in input.splitlines())


def part2(input):
    return sum(solve(code, 25)
               for code in input.splitlines())


def test_part1():
    assert '<A^A>^^AvvvA' in [ ''.join(p) for p in all_num_paths('029A') ]
    assert shortest_path_length('029A', 2) == 68
    assert solve('029A', 2) == 68 * 29

    assert part1(SAMPLE) == 126384


if __name__ == '__main__':
    inputfile = re.sub(r"^.*?([^/]+)\.py$", r"\1.txt", __file__)
    INPUT = open(inputfile, "r").read()

    result = part1(INPUT)
    print("part1:", result)
    assert result == 137870

    result = part2(INPUT)
    print("part2:", result)
    assert result == 170279148659464

    num, total = timeit.Timer(lambda: part2(INPUT)).autorange()
    print("time=", total / num)
