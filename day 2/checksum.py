#!/usr/bin/env python3
# -*- coding: utf-8 -*

def get_input_from_file(file_name):
    with open(file_name) as f:
         return [line.rstrip() for line in f]


def box_id_has_n_of_any_letter(box_id, n):
    for letter in box_id:
        if box_id.count(letter) == n:
            return True
    return False


def get_checksum(box_ids):
    num_two_letters = 0
    num_three_letters = 0

    for box_id in box_ids:
        if box_id_has_n_of_any_letter(box_id, 2):
            num_two_letters += 1
        if box_id_has_n_of_any_letter(box_id, 3):
            num_three_letters += 1

    return num_two_letters * num_three_letters


def number_of_different_letters(id_a, id_b):
    assert(len(id_a) == len(id_b))

    num = 0
    for i in range(0, len(id_a)):
        if id_a[i] != id_b[i]:
            num += 1

    return num


def get_common_letters(id_a, id_b):
    assert(len(id_a) == len(id_b))

    result = ''
    for i in range(0, len(id_a)):
        if id_a[i] == id_b[i]:
            result +=  id_a[i]

    return result


def get_part_two_answer(box_ids):
    for box_id_a in box_ids:
        for box_id_b in box_ids:
            if number_of_different_letters(box_id_a, box_id_b) == 1:
                return get_common_letters(box_id_a, box_id_b)


def _main():
    box_ids = get_input_from_file('input.txt')

    print('Part 1 answer: {}'.format(get_checksum(box_ids)))
    print('Part 2 answer: {}'.format(get_part_two_answer(box_ids)))

    return 0


if __name__ == '__main__':
    exit(_main())
