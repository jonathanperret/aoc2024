from more_itertools import *

SAMPLE = """3   4
4   3
2   5
1   3
3   9
3   3"""

def parse(input):
    lines = input.splitlines()
    pairs = ([int(x) for x in line.split()] for line in lines)
    left, right = (sorted(l) for l in unzip(pairs))
    return left, right

def part1(input):
    left, right = parse(input)
    distances = [ abs(a - b) for a, b in zip(left, right) ]
    return sum(distances)

def part2(input):
    left, right = parse(input)
    scores = [ a * right.count(a) for a in left ]
    return sum(scores)

INPUT = open("day1.txt", "r").read()

print("part1:", part1(SAMPLE))
print("part1:", part1(INPUT))
print("part2:", part2(SAMPLE))
print("part2:", part2(INPUT))
