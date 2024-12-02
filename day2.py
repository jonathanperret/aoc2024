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

def part1(input):
    levelrows = parse(input)
    okcount = 0
    for levels in levelrows:
        deltas = [ (b - a) for a, b in pairwise(levels) ]
        ok = (all((abs(d) >=1 and abs(d) <=3) for d in deltas)
            and
            (all(d <= 0 for d in deltas) or all(d >= 0 for d in deltas))
        )
        print(deltas, ok)
        if ok:
            okcount += 1
    return okcount

def part2(input):
    levelrows = parse(input)
    okcount = 0
    for levels in levelrows:
        for skip in range(len(levels) + 1):
            partial = [l for i, l in zip(count(), levels) if i is not skip]
            deltas = [ (b - a) for a, b in pairwise(partial) ]
            ok = (all((abs(d) >=1 and abs(d) <=3) for d in deltas)
                and
                (all(d <= 0 for d in deltas) or all(d >= 0 for d in deltas))
            )
            if ok:
                okcount += 1
                break
    return okcount

INPUT = open("day2.txt", "r").read()

print("part1:", part1(SAMPLE))
#print("part1:", part1(INPUT))
print("part2:", part2(SAMPLE))
print("part2:", part2(INPUT))
