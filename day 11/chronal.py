#!/usr/bin/env python3
# -*- coding: utf-8 -*

import numpy


def get_fuel_cell_level(x, y, serial_number):
    rack_id = x + 10
    power_level = rack_id * y
    power_level += serial_number
    power_level *= rack_id
    power_level = int(str(power_level)[-3])
    power_level -= 5
    return power_level


def get_square_fuel_cell_level(grid, x_square, y_square, size=3):
    square = grid[y_square:y_square + size, x_square:x_square + size]
    return square.sum()


def fill_fuel_cell_grid(grid, size, serial_number):
    for y in range(size):
        for x in range(size):
            grid[x, y] = get_fuel_cell_level(x, y, serial_number)


def get_part_one_answer(grid, grid_size):
    results = []
    for y in range(grid_size - 2):
        for x in range(grid_size - 2):
            level = get_square_fuel_cell_level(grid, x, y)
            results.append((level, (x, y)))
    return max(results)


def get_part_two_answer(grid, grid_size):
    results = []
    for square_size in range(1, 300):
        for y in range(grid_size - square_size - 1):
            for x in range(grid_size - square_size - 1):
                level = get_square_fuel_cell_level(grid, x, y, square_size)
                results.append((level, (x, y, square_size)))
    return max(results)


def _main():
    SERIAL_NUMBER = 7672
    GRID_SIZE = 300

    cell_grid = numpy.zeros((GRID_SIZE, GRID_SIZE))
    fill_fuel_cell_grid(cell_grid, GRID_SIZE, SERIAL_NUMBER)

    print('Part 1 answer: {}'.format(get_part_one_answer(cell_grid, GRID_SIZE)))
    print('Part 2 answer: {}'.format(get_part_two_answer(cell_grid, GRID_SIZE)))

    return 0


if __name__ == '__main__':
    exit(_main())
