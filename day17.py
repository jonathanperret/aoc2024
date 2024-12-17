from itertools import *
from more_itertools import *
import re
from functools import partial, cmp_to_key
from collections import defaultdict
from math import gcd, sqrt
from heapq import *
import timeit
import functools

SAMPLE = """Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""

SAMPLE2 = """Register A: 2024
Register B: 0
Register C: 0

Program: 0,3,5,4,3,0
"""

OPCODES = [ 'adv', 'bxl', 'bst', 'jnz', 'bxc', 'out', 'bdv', 'cdv' ]

def part1(input):
    ra, rb, rc, *program = map(int, re.findall(r"\d+", input))
    output = []
    pc = 0
    argstr = ['']
    def combo(arg):
        if arg < 4:
            return arg
        argstr[0] = 'abc'[arg - 4]
        return [ra, rb, rc][arg - 4]

    while pc < len(program) - 1:
        opcode = program[pc]
        arg = program[pc + 1]
        argstr[0] = str(arg)
        pc += 2
        match opcode:
            case 0:
                ra //= 2 ** combo(arg)
            case 1:
                rb ^= arg
            case 2:
                rb = combo(arg) % 8
            case 3:
                if ra != 0:
                    pc = arg
            case 4:
                rb ^= rc
            case 5:
                output.append(combo(arg) % 8)
            case 6:
                rb = ra // (2 ** combo(arg))
            case 7:
                rc = ra // (2 ** combo(arg))
            case _:
                print(f"unimplemented {opcode}")
                pass
        print(f"{OPCODES[opcode]} {argstr[0]} -> pc={pc} ra={ra} rb={rb} rc={rc}")

    return (','.join(map(str, output)))


def part2(input):
    _, rb0, rc0, *program = map(int, re.findall(r"\d+", input))

    def run(ra, rb, rc):
        output = []
        pc = 0
        argstr = ['']
        def combo(arg):
            if arg < 4:
                return arg
            argstr[0] = 'abc'[arg - 4]
            return [ra, rb, rc][arg - 4]

        while pc < len(program) - 1:
            opcode = program[pc]
            arg = program[pc + 1]
            argstr[0] = str(arg)
            pc += 2
            match opcode:
                case 0:
                    ra //= 2 ** combo(arg)
                case 1:
                    rb ^= arg
                case 2:
                    rb = combo(arg) % 8
                case 3:
                    if ra != 0:
                        pc = arg
                case 4:
                    rb ^= rc
                case 5:
                    output.append(combo(arg) % 8)
                    if output[-1] != program[len(output)-1]:
                        print(f" FAIL: {output[-1]} instead of {program[len(output)-1]}")
                        return False
                case 6:
                    rb = ra // (2 ** combo(arg))
                case 7:
                    rc = ra // (2 ** combo(arg))
                case _:
                    raise Exception(f"unimplemented {opcode}")

            print(f" {OPCODES[opcode]} {argstr[0]} -> pc={pc} ra={ra} rb={rb} rc={rc}")
        if output == program:
            print(" FOUND")
            return True

    if program == [2,4,1,3,7,5,1,5,0,3,4,3,5,5,3,0]:
        def magic(ra):
            d = ra & 7
            out = d ^ 6 ^ ((ra >> (d ^ 3)) & 7)
            return out

        iter = 0
        def solve(a0, pos):
            nonlocal iter
            iter += 1
            if pos < 0:
                return a0
            a0 <<= 3
            target = program[pos]
            for candidate in range(a0, a0 + 8):
                if magic(candidate) == target:
                    good = solve(candidate, pos - 1)
                    if good:
                        return good
            return None

        result = solve(0, len(program)-1)
        # print(f"{iter} calls")
        return result

    for ra0 in range(1000000):
        print(f"TESTING {ra0}...")

        if run(ra0, rb0, rc0):
            break

    return ra0


def test_part1():
    assert part1(SAMPLE) == '4,6,3,5,6,3,5,2,1,0'


def test_part2():
    assert part2(SAMPLE2) == 117440


if __name__ == '__main__':
    inputfile = re.sub(r"^.*?([^/]+)\.py$", r"\1.txt", __file__)
    INPUT = open(inputfile, "r").read()

    result = part1(INPUT)
    print("part1:", result)
    assert result == '6,2,7,2,3,1,6,0,5'

    result = part2(INPUT)
    print("part2:", result, oct(result))
    assert result == 0o6562166052247155
    assert result == 236548287712877

    num, total = timeit.Timer(lambda: part2(INPUT)).autorange()
    print("time=", total / num)
