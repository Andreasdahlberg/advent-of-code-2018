#!/usr/bin/env python3
# -*- coding: utf-8 -*

import string

def get_input_from_file(file_name):
    with open(file_name) as f:
        return f.read().strip()


def remove_sequence(data):

    for x in range(0, len(data) - 1):
        if data[x] == data[x + 1].swapcase():

            del data[x + 1]
            del data[x]
            return True
    return False


def get_part_one_answer(data_string):
    data = list(data_string)

    while (remove_sequence(data)):
        pass

    return len(data)


def get_part_two_answer(data_string):
    results = []

    for unit in string.ascii_lowercase:
        s = data_string.replace(unit, '')
        s = s.replace(unit.upper(), '')

        results.append(get_part_one_answer(s))

    return min(results)


def _main():

    data_string = get_input_from_file('input.txt')
    #data_string = 'dabAcCaCBAcCcaDA'

    print('Part 1 answer: {}'.format(get_part_one_answer(data_string)))
    print('Part 2 answer: {}'.format(get_part_two_answer(data_string)))

    return 0


if __name__ == '__main__':
    exit(_main())
