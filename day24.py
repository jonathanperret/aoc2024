from itertools import *
from more_itertools import *
import re
from functools import partial, cmp_to_key
from collections import defaultdict, Counter
from math import gcd, sqrt
from heapq import *
import timeit
import functools
import networkx as nx
import bisect

SAMPLE = """x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
"""

def compute(wire, rules, initial_values):
    if wire in rules:
        rule = rules[wire]
        match rule[1]:
            case 'AND':
                return compute(rule[0], rules, initial_values) & compute(rule[2], rules, initial_values)
            case 'OR':
                return compute(rule[0], rules, initial_values) | compute(rule[2], rules, initial_values)
            case 'XOR':
                return compute(rule[0], rules, initial_values) ^ compute(rule[2], rules, initial_values)
            case _:
                raise Exception(f"unknown rule {rule[1]}")
    else:
        return initial_values[wire]


def part1(input):
    initials, rules = input.split('\n\n')
    initial_values = {vs[0]: int(vs[1])
                      for line in initials.splitlines()
                      for vs in [line.split(': ')]}
    rules = {vs[4]: (vs[0], vs[1], vs[2])
                     for line in rules.splitlines()
                     for vs in [line.split(' ')]}

    bits = []
    power = 1
    result = 0
    for wire in sorted(rules.keys()):
        if wire.startswith('z'):
            bit = compute(wire, rules, initial_values)
            bits.append(bit)
            result += power * bit
            power *= 2

    return result


def part2(input):
    return 2


def test_part1():
    assert part1(SAMPLE) == 2024


def test_part2():
    assert part2(SAMPLE) == 2


if __name__ == '__main__':
    inputfile = re.sub(r"^.*?([^/]+)\.py$", r"\1.txt", __file__)
    INPUT = open(inputfile, "r").read()

    result = part1(INPUT)
    print("part1:", result)
    # assert result == 1476

    # num, total = timeit.Timer(lambda: part1(INPUT)).autorange()
    # print("time=", total / num)

    # result = part2(INPUT)
    # print("part2:", result)
    # assert result == 'ca,dw,fo,if,ji,kg,ks,oe,ov,sb,ud,vr,xr'

    # num, total = timeit.Timer(lambda: part2(INPUT)).autorange()
    # print("time=", total / num)
