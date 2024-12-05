from itertools import *
from more_itertools import *
import re
from functools import partial, cmp_to_key

SAMPLE = """47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""

def parse(input):
    rules, updates = input.split('\n\n')
    rules = [ list(map(int, line.split("|"))) for line in rules.splitlines() ]
    updates = [ list(map(int, line.split(","))) for line in updates.splitlines() ]
    return rules, updates

def check(update, rules):
    for rule in rules:
        if rule[0] in update and rule[1] in update:
            if update.index(rule[0]) >= update.index(rule[1]):
                return False
    return True

def part1(input):
    rules, updates = parse(input)
    result = 0
    for update in updates:
        if check(update, rules):
            result += update[len(update) // 2]
    return result

def compare(rules, a, b):
    if [a, b] in rules:
        return -1
    if [b, a] in rules:
        return 1
    return 0

def part2(input):
    rules, updates = parse(input)
    result = 0
    sort_key = cmp_to_key(partial(compare, rules))
    for update in updates:
        if not check(update, rules):
            sorted_update = sorted(update, key = sort_key)
            assert check(sorted_update, rules)
            result += sorted_update[len(sorted_update) // 2]
    return result

INPUT = open("day5.txt", "r").read()

print("part1:", part1(SAMPLE))
print("part1:", part1(INPUT))
print("part2:", part2(SAMPLE))
print("part2:", part2(INPUT))
