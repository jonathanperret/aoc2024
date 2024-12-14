from itertools import *
from more_itertools import *
import re
from functools import partial, cmp_to_key
from collections import defaultdict
from math import gcd, sqrt
from heapq import *
import timeit
import functools

SAMPLE = """p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""

def part1(input, width, height):
    robots = [
            tuple(map(int, re.findall(r"-?\d+", line)))
            for line in input.splitlines()
            ]
    steps = 100
    moved = [
        ((px + 100 * vx) % width, (py + 100 * vy) % height)
        for px, py, vx, vy in robots
    ]

    quadrants = [0, 0, 0, 0]
    for px, py in moved:
        if px < width // 2 and py < height // 2:
            quadrants[0] +=1
        if px < width // 2 and py > height // 2:
            quadrants[1] +=1
        if px > width // 2 and py < height // 2:
            quadrants[2] +=1
        if px > width // 2 and py > height // 2:
            quadrants[3] +=1

    return quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]


def part2(input, width, height):
    robots = [
            tuple(map(int, re.findall(r"-?\d+", line)))
            for line in input.splitlines()
            ]
    maxsteps = int(1e6)
    for i in range(1, maxsteps):
        robots = [
            ((px + vx) % width, (py + vy) % height, vx, vy)
            for px, py, vx, vy in robots
        ]
        matrix = []
        for y in range(height):
            matrix.append(width * ['.'])
        for px, py, vx, vy in robots:
            matrix[py][px] = 'X'

        display = '\n'.join(''.join(row) for row in matrix)
        if 'XXXXXXXXX' in display:
            print(f"steps={i}:")
            print(display)
            return i


def test_part1():
    assert part1(SAMPLE, 11, 7) == 12


if __name__ == '__main__':
    INPUT = open("day14.txt", "r").read()

    result = part1(INPUT, 101, 103)
    print("part1:", result)
    assert result == 215476074

    result = part2(INPUT, 101, 103)
    print("part2:", result)
    assert result == 6285

    num, total = timeit.Timer(lambda: part2(INPUT, 101, 103)).autorange()
    print("time=", total / num)
