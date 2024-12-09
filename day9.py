from itertools import *
from more_itertools import *
import re
from functools import partial, cmp_to_key
from collections import defaultdict
from math import gcd

SAMPLE = """2333133121414131402
"""

def parse(input):
    spans = list(map(int, input.strip()))
    blocks = []
    for i, l in enumerate(spans):
        fileid = i // 2 if i % 2 == 0 else -1
        blocks.extend([ fileid ] * l)
    return blocks, spans

def defrag(blocks):
    target = 0
    for source in range(len(blocks) - 1, -1, -1):
        if blocks[source] < 0:
            continue
        while blocks[target] >= 0:
            target += 1
        if target >= source:
            break
        blocks[target] = blocks[source]
        blocks[source] = -1

def checksum(blocks):
    return sum(i * fileid for i, fileid in enumerate(blocks) if fileid >= 0)

def part1(input):
    blocks, _ = parse(input)
    defrag(blocks)
    return checksum(blocks)

def part2(input):
    _, spans = parse(input)
    freespans = []
    files = []
    start = 0
    for i, l in enumerate(spans):
        if i % 2 == 0:
            files.append((start, l))
        else:
            freespans.append((start, l))
        start += l
    for i in reversed(range(len(files))):
        start, length = files[i]
        for fi, (fstart, flen) in enumerate(freespans):
            if fstart >= start:
                break
            if flen >= length:
                if flen == length:
                    del freespans[fi]
                else:
                    freespans[fi] = (fstart + length, flen - length)
                files[i] = (fstart, length)
                break

    blocks = [-1] * sum(spans)
    for i, (start, length) in enumerate(files):
        for j in range(length):
            blocks[start + j] = i

    return checksum(blocks)

if __name__ == '__main__':
    INPUT = open("day9.txt", "r").read()

    result = part1(INPUT)
    print("part1:", result)
    assert result == 6359213660505

    result = part2(INPUT)
    print("part2:", result)
    assert result == 6381624803796
