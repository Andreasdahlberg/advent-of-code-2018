#!/usr/bin/env python3
# -*- coding: utf-8 -*

def get_input_from_file(file_name):
    with open(file_name) as f:
        lines = f.readlines()
        return [int(line) for line in lines]


def get_resulting_frequency(changes):
    return sum(changes)


def get_first_duplicated_frequency(changes):
    freq_sum = 0
    seen_frequency = [0]

    while True:
        for change in changes:
            freq_sum += change
            if freq_sum in seen_frequency:
                return freq_sum
            seen_frequency.append(freq_sum)


def _main():
    changes = get_input_from_file('input.txt')

    print('Part 1 answer: {}'.format(get_resulting_frequency(changes)))
    print('Part 2 answer: {}'.format(get_first_duplicated_frequency(changes)))

    return 0


if __name__ == '__main__':
    exit(_main())
