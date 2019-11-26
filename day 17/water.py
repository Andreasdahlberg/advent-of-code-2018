#!/usr/bin/env python3
# -*- coding: utf-8 -*

from collections import namedtuple
from collections import deque

Coordinate = namedtuple('Coordinate', ['x', 'y'])

ground_map = [[]]

def get_input_from_file(file_name):

    coordinates = []
    with open(file_name) as f:
        lines = f.readlines()

        raw_coordinates = []
        for line in lines:
            coordinates_dict = {}

            for value in line.rstrip().split(','):
                dimension, offset = value.strip().split('=')
                offsets = [int(x) for x in offset.strip().split('..')]
                coordinates_dict[dimension] = offsets

            raw_coordinates.append(coordinates_dict)

        for raw_coordinate in raw_coordinates:
            dimension_prev = {}
            sorted_coordinates = sorted(raw_coordinate.items(), key=lambda kv: len(kv[1]))

            for value in range(sorted_coordinates[1][1][0], sorted_coordinates[1][1][1] + 1):
                coor = {
                    sorted_coordinates[0][0]: sorted_coordinates[0][1][0],
                    sorted_coordinates[1][0]: value

                }

                coordinates.append(Coordinate(**coor))
    return coordinates


def get_y_max(coordinates):
    return max(coordinates, key=lambda coordinate: coordinate.y).y

def get_x_max(coordinates):
    return max(coordinates, key=lambda coordinate: coordinate.x).x

def get_y_min(coordinates):
    return min(coordinates, key=lambda coordinate: coordinate.y).y

def get_x_min(coordinates):
    return min(coordinates, key=lambda coordinate: coordinate.x).x


class Ground(object):
    def __init__(self, clay_coordinates):
        self._OFFSET = 3
        self.water_sources = deque()
        self._clay_coordinates = clay_coordinates

        self._find_max_min_coordinates()
        self._clay_coordinates = self._get_adjusted_clay_coordinates()
        self._reset()

    def _reset(self):
        self._x_size = self._x_max - self._x_min + self._OFFSET
        self._y_size = self._y_max - self._y_min + self._OFFSET

        print('Map size: {} x {}'.format(self._x_size, self._y_size))
        self._map = [[ '.' for x in range(self._x_size)] for y in range(self._y_size)]
        for coordinate in self._clay_coordinates:
            self._map[coordinate.y][coordinate.x] = '#'

    def _find_max_min_coordinates(self):
        self._y_max = get_y_max(self._clay_coordinates)
        self._y_min = 0#get_y_min(self._clay_coordinates)
        self._x_max = get_x_max(self._clay_coordinates)
        self._x_min = get_x_min(self._clay_coordinates)
        print('x({}-{}), y({}-{})'.format(self._x_min, self._x_max, self._y_min, self._y_max))

    def _get_adjusted_clay_coordinates(self):
        adjusted_coordinates = []

        for coordinate in self._clay_coordinates:
            adjusted_coordinates.append(self.get_adjusted_coordinate(coordinate))
        return adjusted_coordinates

    def get_adjusted_coordinate(self, coordinate):
        y = coordinate.y - self._y_min + int(self._OFFSET / 2)
        x = coordinate.x - self._x_min + int(self._OFFSET / 2)
        return (Coordinate(x, y))

    def draw(self):
        for row in self._map:
            print(''.join(row))

    def to_file(self):
        with open('output.txt', 'w') as f:
            for row in self._map:
                f.write(''.join(row))
                f.write('\n')

    def is_sand(self, coordinate, fall=True):
        if fall:
            return self.get_tile(coordinate) == '.' or self.get_tile(coordinate) == '|'
        else:
            return self.get_tile(coordinate) == '.'

    def set_tile(self, coordinate, state):
        self._map[coordinate.y][coordinate.x] = state

    def print_tile(self, coordinate):
        print(self._map[coordinate.y][coordinate.x])

    def get_tile(self, coordinate):
        try:
            return self._map[coordinate.y][coordinate.x]
        except IndexError as e:
            print(e)
            print(coordinate)
            exit(-1)

    def count_tiles(self, tile_types):
        start = get_y_min(self._clay_coordinates)
        end = get_y_max(self._clay_coordinates) + 1

        count = 0
        for row in self._map[start:end]:
            for tile in row:
                if tile in tile_types:
                    count += 1
        return count

    def fall(self, source):
        # Check if the source is submerged
        if self.get_tile(source) == '~':
            return None

        c = source
        while c.y < self._y_size:
            #print(c, self.is_sand(c))

            if self.is_sand(c):
                self.set_tile(c, '|')
                c = Coordinate(c.x, c.y + 1)
            else:
                return c
        return None

    def fill(self, start_coordinate):
        coordinates = []
        water_tile_coordinates = []

        for i in range(0, self._x_max):
            coordinate = Coordinate(start_coordinate.x - i, start_coordinate.y)
            if not self.is_sand(coordinate, True):
                break

            coordinate_down = Coordinate(coordinate.x, coordinate.y + 1)
            if self.is_sand(coordinate_down, True):
                coordinates.append(coordinate)
                break
            water_tile_coordinates.append(coordinate)

        for i in range(1, self._x_max):
            coordinate = Coordinate(start_coordinate.x + i, start_coordinate.y)
            if not self.is_sand(coordinate, True):
                break

            coordinate_down = Coordinate(coordinate.x, coordinate.y + 1)
            if self.is_sand(coordinate_down, True):
                coordinates.append(coordinate)
                break
            water_tile_coordinates.append(coordinate)

        # No new source coordinates means that the water level has settled
        if not coordinates:
            for tile_coordinate in water_tile_coordinates:
                self.set_tile(tile_coordinate, '~')
        else:
            for tile_coordinate in water_tile_coordinates:
                self.set_tile(tile_coordinate, '|')

        return coordinates

    def __str__(self):
        return 'Ground()'


def _main():
    clay_coordinates = get_input_from_file('input.txt')

    ground = Ground(clay_coordinates)
    water_source = ground.get_adjusted_coordinate(Coordinate(x=500, y=0))
    ground.water_sources.append(water_source)

    source = ground.water_sources.popleft()

    for _ in range(0, 10000):
        clay = ground.fall(source)

        if clay:
            new_sources = ground.fill(Coordinate(clay.x, clay.y - 1))
            if new_sources:
                for new_source in new_sources:
                    ground.water_sources.append(new_source)
            ground.water_sources.appendleft(source)

        if len(ground.water_sources) > 0:
            source = ground.water_sources.pop()
        else:
            break

    ground.to_file()

    print()
    print('Part 1 answer: {}'.format(ground.count_tiles(['|', '~'])))
    print('Part 2 answer: {}'.format(ground.count_tiles(['~'])))

    return 0


if __name__ == '__main__':
    exit(_main())

