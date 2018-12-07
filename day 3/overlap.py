#!/usr/bin/env python3
# -*- coding: utf-8 -*

from collections import namedtuple
import re

FABRIC_SIZE = 1000

def line_to_claim(line):
    Claim = namedtuple('Claim', ['id', 'x', 'y', 'width', 'height'])
    pattern = re.compile('(?P<ID>\d*)\s@\s(?P<x>\d*),(?P<y>\d*):\s(?P<width>\d*)x(?P<height>\d*)')
    match = pattern.search(line.rstrip())
    return Claim(*[int(value) for value in match.groups()])


def get_input_from_file(file_name):
    with open(file_name) as f:
        lines = f.readlines()
        return [line_to_claim(line) for line in lines]


def get_number_of_overlapping_inches(fabric):
    overlapping_inches = 0
    for x in range(0, FABRIC_SIZE):
        for y in range(0, FABRIC_SIZE):
            if fabric[y][x] > 1:
                overlapping_inches += 1

    return overlapping_inches


def mark_claims_on_fabric(fabric, claims):
    for claim in claims:
        for x in range(claim.x, claim.x + claim.width):
            for y in range(claim.y, claim.y + claim.height):
                fabric[y][x] += 1


def is_claim_unique(fabric, claim):
    for x in range(claim.x, claim.x + claim.width):
        for y in range(claim.y, claim.y + claim.height):
            if fabric[y][x] > 1:
                return False
    return True


def get_unique_claim_id(fabric, claims):
   for claim in claims:
        if is_claim_unique(fabric, claim):
            return claim.id


def _main():
    fabric = [[ 0 for y in range(FABRIC_SIZE)] for x in range(FABRIC_SIZE)]
    claims = get_input_from_file('input.txt')

    mark_claims_on_fabric(fabric, claims)

    print('Part 1 answer: {}'.format(get_number_of_overlapping_inches(fabric)))
    print('Part 2 answer: {}'.format(get_unique_claim_id(fabric, claims)))

    return 0


if __name__ == '__main__':
    exit(_main())
