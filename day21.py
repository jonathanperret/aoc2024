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

def keypad_paths(previous_key, key):
    paths = nx.all_shortest_paths(numpad, source=previous_key, target=key)
    return [
        [numpad.get_edge_data(old, new)['direction']
         for old, new in pairwise(path)] + ['A']
        for path in paths
    ]


def dirpad_paths(previous_key, key):
    if key == previous_key:
        return [['A']]

    paths = nx.all_shortest_paths(dirpad, source=previous_key, target=key)
    return [
        [dirpad.get_edge_data(old, new)['direction']
         for old, new in pairwise(path)] + ['A']
        for path in paths
    ]


def best_dir2_path(dir2_key):
    dir2_paths = dirpad_paths(dir2_key)
    for dir2_path in dir2_paths:
        result = []

        return dir2_path


@functools.cache
def best_dir1_path(dir1_previous_key, dir1_key):
    print(f" dir1 optimizing {dir1_previous_key} -> {dir1_key}")
    dir1_paths = dirpad_paths(dir1_previous_key, dir1_key)
    print(f" dir1 options are: { ', '.join([ ''.join(p) for p in dir1_paths ]) }")
    for dir1_path in dir1_paths:
        print(f" dir1 testing { ''.join(dir1_path) }")
        result = dir1_path
        print(f" dir1 returning { ''.join(result) }")
        return result

        for dir2_key in dir1_path:
            print(f"  {dir2_key}")
            dir2_path = best_dir2_path(dir2_key)
            print('   dir2', dir2_path)
            result.extend(dir2_path)
        return result


def best_num_path(num_previous_key, num_key):
    print(f"num optimizing {num_previous_key} -> {num_key}")
    num_paths = keypad_paths(num_previous_key, num_key)
    print(f"num options are: { ', '.join([ ''.join(p) for p in num_paths ]) }")
    for num_path in num_paths:
        print(f"num testing { ''.join(num_path) }")
        result = []
        for dir1_prev_key, dir1_key in pairwise(['A'] + num_path):
            dir1_path = best_dir1_path(dir1_prev_key, dir1_key)
            print(f"num best dir1 for {dir1_prev_key} -> {dir1_key} is {''.join(dir1_path)}")
            result.extend(dir1_path)
        print(f"result { ''.join(result) }")
        return result

    return 1


def part1(input):
    return sum(solve(code)
               for code in input.splitlines())


def part2(input):
    return 2;


def all_num_paths(code):
    result = [[]]
    for old, new in pairwise(['A'] + list(code)):
        paths = keypad_paths(old, new)
        newresult = []
        for p in paths:
            for r in result:
                newresult.append(r + p)
        result = newresult
    return result


def all_dir_paths(dirs):
    result = [[]]
    for old, new in pairwise(['A'] + list(dirs)):
        paths = dirpad_paths(old, new)
        newresult = []
        for p in paths:
            for r in result:
                newresult.append(r + p)
        result = newresult
    return result

def all_dir2_paths(dirs):
    return ( p2
            for p in all_dir_paths(dirs)
            for p2 in all_dir_paths(''.join(p))
            )


def all_num2_paths(code):
    paths = ( p2
            for p in all_num_paths(code)
            for p2 in all_dir2_paths(''.join(p))
             )
    return paths

def shortest_path_length(code):
    return min(len(p) for p in all_num2_paths(code))

def solve(code):
    print(f"solving {code}")
    return shortest_path_length(code) * int(code[:-1])


def test_part1():
    assert '<A^A>^^AvvvA' in [ ''.join(p) for p in all_num_paths('029A') ]
    assert 'v<<A>>^A<A>AvA<^AA>A<vAAA>^A' in ( ''.join(p) for p in all_dir_paths('<A^A>^^AvvvA') )
    assert '<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A' \
            in ( ''.join(p) for p in all_dir_paths('v<<A>>^A<A>AvA<^AA>A<vAAA>^A') )
    assert '<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A' \
            in ( ''.join(p) for p in all_dir2_paths('<A^A>^^AvvvA') )
    assert '<vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A' \
            in ( ''.join(p) for p in all_num2_paths('029A') )
    assert shortest_path_length('029A') == 68
    assert solve('029A') == 68 * 29

    assert part1(SAMPLE) == 126384


def test_part2():
    assert part2(SAMPLE) == 2


if __name__ == '__main__':
    inputfile = re.sub(r"^.*?([^/]+)\.py$", r"\1.txt", __file__)
    INPUT = open(inputfile, "r").read()

    result = part1(INPUT)
    print("part1:", result)
    # assert result == 1521

    # result = part2(INPUT)
    # print("part2:", result)
    # assert result == 1013106

    # num, total = timeit.Timer(lambda: part2(INPUT)).autorange()
    # print("time=", total / num)
