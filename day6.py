from itertools import *
from more_itertools import *
import re
from functools import partial, cmp_to_key

SAMPLE = """....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

def parse(input):
    matrix = input.splitlines()
    obstacles = set()
    for i, row in enumerate(matrix):
        for j, cell in enumerate(row):
            if cell == '#':
                obstacles.add((i, j))
            elif cell == '^':
                initialpos = (i, j)
    return initialpos, len(matrix[0]), len(matrix), obstacles

def dump(pos, width, height, obstacles, visited):
    matrix = [
        [
            '#' if (i, j) in obstacles
            else 'X' if (i, j) in visited
            else '.'
            for j in range(width)
        ]
        for i in range(height)
    ]
    print('\n'.join(''.join(row) for row in matrix))
    print('---')

def part1(input):
    pos, width, height, obstacles = parse(input)
    direction = (-1, 0)
    visited = set()
    while pos[0] >= 0 and pos[0] < height and pos[1] >= 0 and pos[1] < width:
        visited.add(pos)
        nextpos = ( pos[0] + direction[0], pos[1] + direction[1] )
        if nextpos in obstacles:
            direction = ( direction[1], -direction[0] )
        else:
            pos = nextpos

    dump(pos, width, height, obstacles, visited)

    return len(visited)

def check(initial_pos, width, height, obstacles):
    pos = initial_pos
    direction = (-1, 0)
    visited = set()
    while pos[0] >= 0 and pos[0] < height and pos[1] >= 0 and pos[1] < width:
        posdir = (pos, direction)
        if posdir in visited:
            return True
        visited.add(posdir)
        nextpos = ( pos[0] + direction[0], pos[1] + direction[1] )
        if nextpos in obstacles:
            direction = ( direction[1], -direction[0] )
        else:
            pos = nextpos
    return False

def part2(input):
    initial_pos, width, height, obstacles = parse(input)
    loopers = set()
    pos = initial_pos
    direction = (-1, 0)
    while pos[0] >= 0 and pos[0] < height and pos[1] >= 0 and pos[1] < width:
        if pos != initial_pos \
           and pos not in loopers \
           and check(initial_pos, width, height, obstacles.union([pos])):
            print("looping with ", nextpos)
            loopers.add(pos)
        nextpos = ( pos[0] + direction[0], pos[1] + direction[1] )
        if nextpos in obstacles:
            direction = ( direction[1], -direction[0] )
        else:
            pos = nextpos

    # dump(pos, width, height, obstacles, set(v[0] for v in visited))

    return len(loopers)

INPUT = open("day6.txt", "r").read()

# print("part1:", part1(SAMPLE))
# print("part1:", part1(INPUT))
print("part2:", part2(SAMPLE))
print("part2:", part2(INPUT))
