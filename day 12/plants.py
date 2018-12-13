#!/usr/bin/env python3
# -*- coding: utf-8 -*

from collections import namedtuple

def get_initial_state_from_text(text):
    initial_state = []
    pot_id = 0
    for char in text:
        initial_state.append((pot_id, char == '#'))
        pot_id += 1
    return initial_state


def get_rule_from_text(text):
    Rule = namedtuple('Rule', ['pattern', 'output', 'new_pattern'])
    pattern, output = text.split(' => ')
    new_pattern = pattern[:2] + output + pattern[3:]
    return Rule(pattern, output, new_pattern)


def get_input_from_file(file_name):
    with open(file_name) as f:
        lines = f.readlines()
        initial_state = lines[0].split(':')[1].strip()
        return initial_state, [get_rule_from_text(line.rstrip()) for line in lines[2:]]


def sum_pot_numbers(pot_state, offset):
    pot_sum = 0
    for i in range(0, len(pot_state)):
        if pot_state[i] == '#':
            pot_sum += (i + offset)

    return pot_sum


def get_part_one_answer():
    pot_state, rules = get_input_from_file('input.txt')

    offset = -20
    pot_state = 20* '.' + pot_state + '...'

    for gen in range(0, 20):
        new_state = list(len(pot_state) * '.')
        for rule in rules:
            for i in range(0, len(pot_state) - 2):
                pot_slice = pot_state[i: i + 5]
                current_pot_index = i + 2

                if len(pot_slice) < 5:
                    pot_slice = pot_slice + '.' * (5 - len(pot_slice))

                if pot_slice == rule.pattern:
                    new_state[current_pot_index] = rule.output

        pot_state = ''.join(new_state)
        if pot_state[-1] == '#':
            pot_state = pot_state + '..'
        elif pot_state[-2] == '#':
            pot_state = pot_state + '.'

    return sum_pot_numbers(pot_state, offset)


def get_part_two_answer():
    # The following pattern is repeated with an offset in each generation.
    st = '###..###..###..###..###..###..###..###..###..###..###..###..###..###..###..###..###..###..###..###..###..###..###..###..###..###..###..###..###..###..###..###..###..###.'
    return sum_pot_numbers(st, 50000000000 - 70)


def _main():

    print('Part 1 answer: {}'.format(get_part_one_answer()))
    print('Part 2 answer: {}'.format(get_part_two_answer()))

    return 0


if __name__ == '__main__':
    exit(_main())
