from itertools import *
from more_itertools import *

SAMPLE = """7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9"""

def parse(input):
    lines = input.splitlines()
    levelrows = ([int(x) for x in line.split()] for line in lines)
    return levelrows

def checklevels(levels):
    deltas = [ (b - a) for a, b in pairwise(levels) ]
    ok = (all((abs(d) >=1 and abs(d) <=3) for d in deltas)
        and
        (all(d <= 0 for d in deltas) or all(d >= 0 for d in deltas))
    )
    return ok

def part1(input):
    levelrows = parse(input)
    return quantify(levelrows, checklevels)

def except_nth(it, n):
    return (x for i, x in zip(count(), it) if i is not n)

def part2(input):
    levelrows = parse(input)
    return quantify(
        any(checklevels(except_nth(levels, skip))
            for skip in range(len(levels) + 1))
        for levels in levelrows
    )

INPUT = open("day2.txt", "r").read()

print("part1:", part1(SAMPLE))
print("part1:", part1(INPUT))
print("part2:", part2(SAMPLE))
print("part2:", part2(INPUT))
