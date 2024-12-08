from itertools import *
from more_itertools import *
import re
from functools import partial, cmp_to_key
from collections import defaultdict
from math import gcd

SAMPLE = """............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""

def parse(input):
    lines = input.splitlines()
    antennas = defaultdict(list)
    for i, row in enumerate(lines):
        for j, cell in enumerate(row):
            if cell != '.':
                antennas[cell].append((i, j))

    return antennas, len(lines), len(lines[0])

def part1(input):
    antennas, height, width = parse(input)
    antinodes = set()
    for freq, ants in antennas.items():
        pairs = [ (a, b) for a in ants for b in ants if a != b ]
        for a, b in pairs:
            node = ( 2 * b[0] - a[0], 2 * b[1] - a[1] )
            if node[0] >= 0 and node[1] >= 0 \
               and node[0] < height and node[1] < width:
                antinodes.add(node)

    return len(antinodes)

def part2(input):
    antennas, height, width = parse(input)
    antinodes = set()
    for freq, ants in antennas.items():
        pairs = [ (a, b) for a in ants for b in ants if a != b ]
        for a, b in pairs:
            d = gcd(b[0] - a[0], b[1] - a[1])
            step = ( (b[0] - a[0]) / d,  (b[1] - a[1]) / d )
            node = a
            while node[0] >= 0 and node[1] >= 0 \
               and node[0] < height and node[1] < width:
                antinodes.add(node)
                node = ( node[0] + step[0], node[1] + step[1] )

    return len(antinodes)

if __name__ == '__main__':
    INPUT = open("day8.txt", "r").read()

    result = part1(INPUT)
    print("part1:", result)
    assert result == 247

    result = part2(INPUT)
    print("part2:", result)
    assert result == 861
