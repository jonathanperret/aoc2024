from itertools import *
from more_itertools import *
import re

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

def reorder(update, rules):
    used_rules = []
    for rule in rules:
        if rule[0] in update and rule[1] in update:
            used_rules.append(rule)
    result = []
    rights = set( rule[1] for rule in used_rules )
    while len(result) < len(update):
        for left, right in used_rules:
            if left not in result and left not in rights:
                result.append(left)
                rights = set( rule[1] for rule in used_rules if rule[0] not in result )
                break
        if len(rights) == 0:
            result.extend(l for l in update if l not in result)
    return result

def part2(input):
    rules, updates = parse(input)
    result = 0
    for update in updates:
        if not check(update, rules):
            sorted_update = reorder(update, rules)
            assert check(sorted_update, rules)
            result += sorted_update[len(sorted_update) // 2]
    return result

INPUT = open("day5.txt", "r").read()

print("part1:", part1(SAMPLE))
print("part1:", part1(INPUT))
print("part2:", part2(SAMPLE))
print("part2:", part2(INPUT))
