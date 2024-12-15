from itertools import *
from more_itertools import *
import re
from functools import partial, cmp_to_key
from collections import defaultdict
from math import gcd, sqrt
from heapq import *
import timeit
import functools

SAMPLE1 = """########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
"""

SAMPLE2 = """##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""

def parse(input):
    matrixlines, movelines = input.split('\n\n')
    matrix = matrixlines.splitlines()
    height = len(matrix)
    width = len(matrix[0])
    walls = set()
    boxes = set()
    for i, row in enumerate(matrix):
        for j, cell in enumerate(row):
            if cell == '@':
                startpos = (i, j)
            elif cell == '#':
                walls.add((i, j))
            elif cell == 'O':
                boxes.add((i, j))
    moves = [ m
              for line in movelines.splitlines()
              for m in line ]
    return (startpos, boxes, walls, width, height, moves)

def score(boxes):
    return sum(
            i * 100 + j
            for (i, j) in boxes
            )

def trymove(i, j, di, dj, boxes, walls):
    if (i, j) in walls:
        print("blocked")
        return False
    if (i, j) not in boxes:
        print("done")
        return True
    # print(f"trying to move {i},{j} by {di},{dj} to {i+di},{j+dj}")
    if not trymove(i+di, j+dj, di, dj, boxes, walls):
        return False
    boxes.remove((i, j))
    boxes.add((i+di, j+dj))
    return True


def part1(input):
    startpos, boxes, walls, width, height, moves = parse(input)
    i, j = startpos

    for move in moves:
        if move == '^':
            di, dj = (-1, 0)
        elif move == 'v':
            di, dj = (1, 0)
        elif move == '<':
            di, dj = (0, -1)
        elif move == '>':
            di, dj = (0, 1)
        # print("from", i, j, di, dj, boxes, move)
        if (i+di, j+dj) in walls:
            # print("bump")
            continue
        if trymove(i+di, j+dj, di, dj, boxes, walls):
            i += di
            j += dj
        # print(i, j, di, dj, boxes)

    return score(boxes)

def part2(input):
    return 2

def test_part1_1():
    assert part1(SAMPLE1) == 2028

def test_part1_2():
    assert part1(SAMPLE2) == 10092

def test_part2():
    assert part2(SAMPLE2) == 9021

if __name__ == '__main__':
    INPUT = open("day15.txt", "r").read()

    result = part1(INPUT)
    print("part1:", result)
    assert result == 1383666

    result = part2(INPUT, 101, 103)
    print("part2:", result)
#    assert result == 6285
#
#    num, total = timeit.Timer(lambda: part2(INPUT, 101, 103)).autorange()
#    print("time=", total / num)
