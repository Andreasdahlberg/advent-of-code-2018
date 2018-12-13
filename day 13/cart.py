#!/usr/bin/env python3
# -*- coding: utf-8 -*

from collections import namedtuple

Coordinate = namedtuple('Coordinate', ['x', 'y'])

class Cart(object):
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction

        self._direction_counter = 0
        self.crashed = False

    def __repr__(self):
        return 'Cart({},{},{},{})'.format(self.x, self.y, self.direction, self.crashed)

    def __str__(self):
        return 'Cart({},{},{},{})'.format(self.x, self.y, self.direction, self.crashed)

    def update_direction(self, track_part):
        intersection = [
            {
                '^': '<',
                'v': '>',
                '>': '^',
                '<': 'v',
            },
            {
                '^': '^',
                'v': 'v',
                '>': '>',
                '<': '<',
            },
            {
                '^': '>',
                'v': '<',
                '>': 'v',
                '<': '^',
            }
        ]

        curve = {
            '/': {
                '^': '>',
                'v': '<',
                '<': 'v',
                '>': '^',
            },
            '\\': {
                '^': '<',
                'v': '>',
                '<': '^',
                '>': 'v',
            }
        }

        if track_part == '+':
            self.direction = intersection[self._direction_counter][self.direction]
            self._direction_counter += 1
            if self._direction_counter > 2:
                self._direction_counter = 0
        elif track_part == '/' or track_part == '\\':
            self.direction = curve[track_part][self.direction]

    def update_position(self):
        moves = {
        '^': Coordinate(0, -1),
        'v': Coordinate(0, 1),
        '>': Coordinate(1, 0),
        '<': Coordinate(-1, 0)
        }

        self.x += moves[self.direction].x
        self.y += moves[self.direction].y


def get_input_from_file(file_name):
    with open(file_name) as f:
        lines = f.readlines()
        return [line.rstrip() for line in lines]


def is_cart(char):
    directions = ['^', 'v', '<', '>']
    return char in directions


def get_carts(track_data):
    carts = []

    for y in range(len(track_data)):
        for x in range(len(track_data[y])):
            char = track_data[y][x]

            if is_cart(char):
                carts.append(Cart(x, y, char))
    return carts


def has_crashed(cart_a, cart_b):
    return cart_a.x == cart_b.x and cart_a.y == cart_b.y


def check_for_collisions(carts, current_cart):
    for cart in carts:
        if cart != current_cart and not cart.crashed:
            if has_crashed(cart, current_cart):
                return(cart, current_cart)
    return None


def count_remaining_carts(carts):
    count = 0
    for cart in carts:
        if not cart.crashed:
            count += 1
    return count


def get_remaining_carts(carts):
    remaining_carts = []
    for cart in carts:
        if not cart.crashed:
            remaining_carts.append(cart)
    return remaining_carts


def get_part_one_answer(track_data):
    carts = get_carts(track_data)

    while True:
        carts.sort(key=lambda cart: (cart.y, cart.x))
        for cart in carts:
            cart.update_position()
            cart.update_direction(track_data[cart.y][cart.x])
            crashed_carts = check_for_collisions(carts, cart)
            if (crashed_carts):
                return Coordinate(crashed_carts[0].x, crashed_carts[0].y)


def get_part_two_answer(track_data):
    carts = get_carts(track_data)

    while(count_remaining_carts(carts) > 1):
        carts.sort(key=lambda cart: (cart.y, cart.x))

        for cart in carts:
            if not cart.crashed:
                cart.update_position()
                cart.update_direction(track_data[cart.y][cart.x])
                crashed_carts = check_for_collisions(carts, cart)
                if (crashed_carts):
                    crashed_carts[0].crashed = True
                    crashed_carts[1].crashed = True

        remaining_carts = get_remaining_carts(carts)

    if remaining_carts:
        return Coordinate(remaining_carts[0].x, remaining_carts[0].y)
    else:
        return None


def _main():
    track_data = get_input_from_file('input.txt')

    print('Part 1 answer: {}'.format(get_part_one_answer(track_data)))
    print('Part 2 answer: {}'.format(get_part_two_answer(track_data)))

    return 0


if __name__ == '__main__':
    exit(_main())
