from itertools import *
from more_itertools import *
import re
from functools import partial, cmp_to_key
from collections import defaultdict
from math import gcd
from heapq import *
import timeit

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
    spans = list(map(int, input.strip()))

    files = []
    freedict = defaultdict(list)
    start = 0
    for i, l in enumerate(spans):
        if i % 2 == 0:
            files.append((start, l))
        else:
            freedict[l].append(start)
        start += l

    for fileid in reversed(range(len(files))):
        start, length = files[fileid]
        best = min(((ss[0], l) for l, ss in freedict.items()
                    if l >= length and len(ss)>0 and ss[0] < start),
                   key=lambda p: p[0], default=None)
        if best:
            beststart, bestlen = best
            files[fileid] = (beststart, length)
            heappop(freedict[bestlen])
            remaininglen = bestlen - length
            if remaininglen > 0:
                heappush(freedict[remaininglen], beststart + length)

    csum = sum(fileid * (start * length + length * (length - 1) // 2)
               for fileid, (start, length) in enumerate(files))

    return csum

if __name__ == '__main__':
    INPUT = open("day9.txt", "r").read()

    result = part1(INPUT)
    print("part1:", result)
    assert result == 6359213660505

    result = part2(INPUT)
    print("part2:", result)
    assert result == 6381624803796

    num, total = timeit.Timer(lambda: part2(INPUT)).autorange()
    print("time=", total / num)
