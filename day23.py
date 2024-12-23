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

SAMPLE = """kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
"""

def parse(input):
    pairs = [ line.split('-') for line in input.splitlines() ]
    g = nx.Graph()
    for a,b in pairs: g.add_edge(a, b)
    return g


def part1(input):
    P = 26
    P2 = P*P

    def O(a):
        return ord(a)-97

    edges = sorted(
            P2 * (P * O(a[0]) + O(a[1])) + (P * O(b[0]) + O(b[1]))
            for a, b in (sorted(line.split('-')) for line in input.splitlines()))

    result = 0
    for ab in edges:
        a, b = divmod(ab, P2)
        hast = P*O('t') <= a < P*O('u') or P*O('t') <= b < P*O('u')
        for bc in edges[
                bisect.bisect_left(edges, P2*b +  (O('t')*P if not hast else 0))
                :
                bisect.bisect_right(edges, P2*b +  (O('u')*P-1 if not hast else P2))
            ]:
            ac = (a - b) * P2 + bc
            if edges[bisect.bisect_left(edges, ac)] == ac:
                result += 1

    return result


def part2(input):
    g = parse(input)

    cliques = nx.find_cliques(g)
    return ','.join(sorted(max(cliques, key=len)))


def test_part1():
    assert part1(SAMPLE) == 7


def test_part2():
    assert part2(SAMPLE) == 'co,de,ka,ta'


if __name__ == '__main__':
    inputfile = re.sub(r"^.*?([^/]+)\.py$", r"\1.txt", __file__)
    INPUT = open(inputfile, "r").read()

    result = part1(INPUT)
    print("part1:", result)
    assert result == 1476

    num, total = timeit.Timer(lambda: part1(INPUT)).autorange()
    print("time=", total / num)

    result = part2(INPUT)
    print("part2:", result)
    assert result == 'ca,dw,fo,if,ji,kg,ks,oe,ov,sb,ud,vr,xr'

    num, total = timeit.Timer(lambda: part2(INPUT)).autorange()
    print("time=", total / num)
