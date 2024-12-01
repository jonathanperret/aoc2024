SAMPLE = """3   4
4   3
2   5
1   3
3   9
3   3"""


def part1(input):
    lines = input.splitlines()
    left = sorted([int(line.split()[0]) for line in lines])
    right = sorted([int(line.split()[1]) for line in lines])
    distances = [ abs(a - b) for a, b in zip(left, right)]
    return sum(distances)

def part2(input):
    lines = input.splitlines()
    left = sorted([int(line.split()[0]) for line in lines])
    right = sorted([int(line.split()[1]) for line in lines])
    scores = [ sum([ a for b in right if a == b ]) for a in left ]
    return sum(scores)

INPUT = open("day1.txt", "r").read()

print("part1:", part1(SAMPLE))
print("part1:", part1(INPUT))
print("part2:", part2(SAMPLE))
print("part2:", part2(INPUT))
