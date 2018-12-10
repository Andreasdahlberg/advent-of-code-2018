#!/usr/bin/env python3
# -*- coding: utf-8 -*

from collections import namedtuple
import re

class Star(object):
    def __init__(self, x, y, x_velocity, y_velocity):
        self.x = x
        self.y = y
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity


def decode_line(line):
    pattern = re.compile('(-?\d+)')
    values = pattern.findall(line.rstrip())

    return Star(*[int(value) for value in values])


def get_input_from_file(file_name):
    with open(file_name) as f:
        lines = f.readlines()
        return [decode_line(line) for line in lines]


def update_star_positions(stars, direction=1):
    for star in stars:
        star.x += star.x_velocity * direction
        star.y += star.y_velocity * direction


def get_max_x(stars):
    max_x = 0
    for star in stars:
        if star.x > max_x:
            max_x = star.x
    return max_x


def get_min_x(stars):
    min_x = 0
    for star in stars:
        if star.x < min_x:
            min_x = star.x

    return min_x


def get_max_y(stars):
    max_y = 0
    for star in stars:
        if star.y > max_y:
            max_y = star.y
    return max_y


def get_min_y(stars):
    min_y = 0
    for star in stars:
        if star.y < min_y:
            min_y = star.y

    return min_y


def get_x_size(stars):
     return get_max_x(stars) + abs(get_min_x(stars)) + 1


def get_y_size(stars):
     return get_max_y(stars) + abs(get_min_y(stars)) + 1


def get_star_area(stars):
    return get_y_size(stars) * get_x_size(stars)


def fill_star_map(star_map, stars):
    for star in stars:
        star_map[star.y][star.x] = '#'


def print_star_map(star_map):
    for y in star_map:
        for x in y:
            print(x, end='')
        print()


def _main():
    stars = get_input_from_file('input.txt')

    max_area = get_star_area(stars)
    for t in range(100000):
        update_star_positions(stars)
        area =  get_star_area(stars)

        if area <= max_area:
            max_area = area
        else:
            # Since the area already has begun to expand we have to rewind one second.
            update_star_positions(stars, -1)

            star_map = [[ '.' for x in range(get_x_size(stars))] for y in range(get_y_size(stars))]

            fill_star_map(star_map, stars)
            print_star_map(star_map)

            print('Got message after {} seconds'.format(t))
            break

    return 0


if __name__ == '__main__':
    exit(_main())
