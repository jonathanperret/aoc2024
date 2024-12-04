from itertools import *
from more_itertools import *
import re

SAMPLE = """MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""

NEEDLE = 'XMAS'

DIRS = [
    (0, 1),
    (0, -1),
    (1, 0),
    (-1, 0),
    (1, 1),
    (1, -1),
    (-1, 1),
    (-1, -1),
]

def check(lines, i, j, width, height, vec):
    for n in range(len(NEEDLE)):
        if i < 0 or i >= height or j < 0 or j >= height:
            return False
        if lines[i][j] != NEEDLE[n]:
            return False
        i += vec[0]
        j += vec[1]
    return True

def part1(input):
    lines = input.splitlines()
    height = len(lines)
    width = len(lines[0])
    count = 0
    for i in range(height):
        for j in range(width):
            for vec in DIRS:
                if check(lines, i, j, width, height, vec):
                    count += 1

    return count

def part2(input):
    lines = input.splitlines()
    height = len(lines)
    width = len(lines[0])
    count = 0
    for i in range(1, height - 1):
        for j in range(1, width - 1):
            if lines[i][j] == 'A':
                diag1 = lines[i-1][j-1] + lines[i][j] + lines[i+1][j+1]
                diag2 = lines[i-1][j+1] + lines[i][j] + lines[i+1][j-1]
                if (diag1 == 'MAS' or diag1 == 'SAM') and (diag2 == 'SAM' or diag2 == 'MAS'):
                    count += 1

    return count

INPUT = open("day4.txt", "r").read()

print("part1:", part1(SAMPLE))
print("part1:", part1(INPUT))
print("part2:", part2(SAMPLE))
print("part2:", part2(INPUT))
