from itertools import *
from more_itertools import *
import re

SAMPLE = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"
SAMPLE2 = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"

def part1(input):
    pat = re.compile("mul\\(([0-9]{1,3}),([0-9]{1,3})\\)")
    matches = pat.findall(input)
    products = [ int(a)*int(b) for a,b in matches]
    return sum(products)

def part2(input):
    pat = re.compile("mul\\(([0-9]{1,3}),([0-9]{1,3})\\)|don'(t)\\(\\)|(d)o\\(\\)")
    matches = pat.findall(input)
    enabled = True
    result = 0
    for m in matches:
        if m[2] == 't':
            enabled = False
        elif m[3] == 'd':
            enabled = True
        elif enabled:
            result += int(m[0]) * int(m[1])
    return result

INPUT = open("day3.txt", "r").read()

print("part1:", part1(SAMPLE))
print("part1:", part1(INPUT))
print("part2:", part2(SAMPLE2))
print("part2:", part2(INPUT))
