from itertools import *
from more_itertools import *
import re
from functools import partial, cmp_to_key
from collections import defaultdict
from math import gcd, sqrt
from heapq import *
import timeit
import functools
import networkx as nx

SAMPLE = """1
10
100
2024
"""

SAMPLE2 = """1
2
3
2024
"""

def make_secret(secret, rounds):
    for _ in range(rounds):
        secret = ((secret << 6) ^ secret) & 0xffffff
        secret = ((secret >> 5) ^ secret)
        secret = ((secret << 11) ^ secret) & 0xffffff
    return secret

def find_period():
    secret = seed = 16777215
    last = 0
    gen = set([secret])
    for i in range(16777217):
        secret = ((secret << 6) ^ secret) & 0xffffff
        secret = ((secret >> 5) ^ secret)
        secret = ((secret << 11) ^ secret) & 0xffffff
        gen.add(secret)
        if secret == seed:
            print(i, len(gen))
            break

# find_period()

def part1(input):
    seeds = map(int, input.splitlines())
    result = 0
    for seed in seeds:
        secret = make_secret(seed, 2000)
        result += secret
    return result

def xorshift(secret):
    secret = ((secret << 6) ^ secret) & 0xffffff
    secret = ((secret >> 5) ^ secret) & 0xffffff
    secret = ((secret << 11) ^ secret) & 0xffffff
    return secret


def checksecret(trace, secret):
    testtrace = 0
    for _ in range(10):
        secret = xorshift(secret)
        testtrace = testtrace * 10 + secret % 10
        if testtrace == trace:
            return
    raise Exception(f"expected {testtrace} == {trace}")

def findsecrets(traces):
    traceset = set(traces)
    mask = 10**8
    secret = last = 1
    secretdict = {}
    secretseq = []
    for i in range(16777217 + 1000):
        secretseq.append(secret)
        secret = ((secret << 6) ^ secret) & 0xffffff
        secret = ((secret >> 5) ^ secret) & 0xffffff
        secret = ((secret << 11) ^ secret) & 0xffffff
        last = (last * 10 + (secret % 10)) % mask
        if last in traceset:
            secretdict[last] = secretseq[i - 7]
            traceset.remove(last)
        elif (last % 10000000) in traceset:
            secretdict[last % 10000000] = secretseq[i - 6]
            traceset.remove(last % 10000000)
        elif (last % 1000000) in traceset:
            secretdict[last % 1000000] = secretseq[i - 5]
            traceset.remove(last % 1000000)
        else:
            continue
        # print(i, last, secret)

    print(f"found {len(secretdict)} secrets, remaining {len(traceset)}")

    for trace, secret in secretdict.items():
        checksecret(trace, secret)

    return secretdict


def optimize(secrets):
    seqdicts = []
    allseqs = set()
    for monkey, secret in enumerate(secrets):
        prices = []
        seq = []
        seqdict = defaultdict(lambda: 0)
        price = secret % 10
        for i in range(2000):
            secret = xorshift(secret)
            old, price = price, secret % 10
            seq.append(price - old)
            if len(seq) > 4:
                seq[:1] = []
            if len(seq) == 4:
                seqt = tuple(seq)
                if seqt not in seqdict:
                    seqdict[seqt] = price
                    allseqs.add(seqt)
        seqdicts.append(seqdict)

    print(f"found {len(allseqs)} different sequences")

    grosses = (sum(seqdict[seq]
                    for seqdict in seqdicts)
               for seq in allseqs)

    return max(grosses)


def part2(input):
    secrets = map(int, input.splitlines())

    return optimize(secrets)


def test_part1():
    assert part1(SAMPLE) == 37327623


def test_part2():
    assert part2(SAMPLE2) == 23


if __name__ == '__main__':
    inputfile = re.sub(r"^.*?([^/]+)\.py$", r"\1.txt", __file__)
    INPUT = open(inputfile, "r").read()

    result = part1(INPUT)
    print("part1:", result)
    assert result == 13753970725

    result = part2(INPUT)
    print("part2:", result)
    # assert result == 170279148659464

    # num, total = timeit.Timer(lambda: part2(INPUT)).autorange()
    # print("time=", total / num)
