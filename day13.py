from itertools import *
from more_itertools import *
import re
from functools import partial, cmp_to_key
from collections import defaultdict
from math import gcd, sqrt
from heapq import *
import timeit
import functools

SAMPLE = """Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""

def parse(input):
    return [tuple(tuple(map(int,re.findall(r"\d+", line)))
            for line in block.splitlines())
            for block in input.split("\n\n")]


def intersect(dxa, dya, x0b, y0b, dxb, dyb):
    num = dyb * x0b - dxb * y0b
    denom = dxa * dyb - dxb * dya
    x, rx = divmod(dxa * num, denom)
    y, ry = divmod(dya * num, denom)
    if rx == 0 and ry == 0:
        return (x, y)
    return None


def solve(machine):
    (ax, ay), (bx, by), (tx, ty) = machine
    inter = intersect(ax, ay, tx, ty, bx, by)
    if not inter:
        return 0
    ix, iy = inter
    a, ra = divmod(ix, ax)
    if ra != 0:
        return 0
    b, rb = divmod(tx - ix, bx)
    if rb != 0:
        return 0

    assert (a * ax + b * bx, a * ay + b * by) == (tx, ty)
    return a * 3 + b


def part1(input):
    machines = parse(input)
    return sum(solve(m) for m in machines)


def part2(input):
    machines = [
        (a, b, (tx + 10000000000000, ty + 10000000000000))
        for a, b, (tx, ty) in parse(input)
    ]
    return sum(solve(m) for m in machines)


def test_part1():
    assert part1(SAMPLE) == 480


def test_part2():
    assert part2(SAMPLE) == 875318608908


if __name__ == '__main__':
    INPUT = open("day13.txt", "r").read()

    result = part1(INPUT)
    print("part1:", result)
    assert result == 36250

    result = part2(INPUT)
    print("part2:", result)
    assert result == 83232379451012

    num, total = timeit.Timer(lambda: part2(INPUT)).autorange()
    print("time=", total / num)
