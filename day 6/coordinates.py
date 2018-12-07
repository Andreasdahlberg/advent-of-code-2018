#!/usr/bin/env python3
# -*- coding: utf-8 -*

from collections import namedtuple

Coordinate = namedtuple('Coordinate', ['x', 'y'])

def get_input_from_file(file_name):

    with open(file_name) as f:
        return [Coordinate(*[int(c) for c in line.rstrip().split(', ')]) for line in f.readlines()]


def get_manhattan_distance(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)


def get_max_coordinate(coordinate):
    return max([coordinate.x, coordinate.y])


def get_coordinate_map_size(coordinates):
    coordinate = max(coordinates, key=get_max_coordinate)
    return get_max_coordinate(coordinate)


def is_on_map_edge(x, y, size):
    return x == 0 or y == 0 or x == size - 1 or  x == size - 1


def get_coordinate_area(coordinate_map, size, coordinate):
        count = 0
        for y in range(0, size):
            for x in range(0, size):
                if coordinate_map[y][x].closest_coordinate == coordinate and not coordinate_map[y][x].equal:
                    if not is_on_map_edge(x, y, size):
                        count += 1
                    else:
                        return None
        return count


def get_part_one_answer(coordinates):
    MapCoordinate = namedtuple('MapCoordinate', ['distance', 'closest_coordinate', 'equal'])

    coordinate_map_size = get_coordinate_map_size(coordinates)
    coordinate_map = [[ None for y in range(coordinate_map_size)] for x in range(coordinate_map_size)]

    for y in range(0, coordinate_map_size):
        for x in range(0, coordinate_map_size):
            for coordinate in coordinates:
                check_coordinate = Coordinate(x, y)
                manhattan_distance = get_manhattan_distance(check_coordinate, coordinate)

                if coordinate_map[y][x] is None or manhattan_distance < coordinate_map[y][x][0]:
                    coordinate_map[y][x] = MapCoordinate(manhattan_distance, coordinate, False)
                elif  manhattan_distance == coordinate_map[y][x][0]:
                    coordinate_map[y][x] = MapCoordinate(manhattan_distance, coordinate, True)

    areas = []
    for coordinate in coordinates:
        area = get_coordinate_area(coordinate_map, coordinate_map_size, coordinate)
        if area:
            areas.append(area)

    return max(areas)


def get_part_two_answer(coordinates):
    coordinate_map_size = get_coordinate_map_size(coordinates)

    result = []
    for y in range(0, coordinate_map_size):
        for x in range(0, coordinate_map_size):
            distance_sum = 0
            for coordinate in coordinates:
                distance_sum += get_manhattan_distance(Coordinate(x, y), coordinate)
            result.append((Coordinate(x, y), distance_sum))

    return len([x for x in result if x[1] < 10000])

def _main():
    data = get_input_from_file('input.txt')

    print('Part 1 answer: {}'.format(get_part_one_answer(data)))
    print('Part 2 answer: {}'.format(get_part_two_answer(data)))

    return 0


if __name__ == '__main__':
    exit(_main())
