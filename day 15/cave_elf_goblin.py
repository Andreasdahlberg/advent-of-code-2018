#!/usr/bin/env python3
# -*- coding: utf-8 -*

from collections import namedtuple
from copy import deepcopy
from multiprocessing import Pool
from itertools import product
from collections import deque

try:
    import curses
    CURSES = True
except:
    CURSES = False

import time


#CURSES = False
Coordinate = namedtuple('Coordinate', ['x', 'y'])

class Unit(object):
    def __init__(self, x, y, unit_type, attack_power=3):
        self.x = x
        self.y = y
        self.hp = 200
        self.unit_type = unit_type
        self.attack_power = attack_power

    def __repr__(self):
        return 'Unit({}, {}, {}, {})'.format(self.x, self.y, self.hp, self.unit_type)

    def get_targets_in_range(self, units):
        units_in_range = []

        for unit in units:
            for coordinate in [
                    Coordinate(self.x, self.y - 1),
                    Coordinate(self.x - 1, self.y),
                    Coordinate(self.x + 1, self.y),
                    Coordinate(self.x, self.y + 1),
            ]:
                if unit.coordinate == coordinate and unit.unit_type != self.unit_type and unit.is_alive():
                        units_in_range.append(unit)

        return units_in_range

    def get_target_in_range(self, units):
        targets = self.get_targets_in_range(units)
        if targets:
            lowest_hp = min(targets, key=lambda x: x.hp).hp
            selected_targets = [target for target in targets if target.hp == lowest_hp]
            selected_targets.sort(key=lambda x: (x.y, x.x))
            return selected_targets[0]
        else:
            return None

    def _get_paths_to_target(self, target, cm):
        paths = []
        paths.append(cm.get_path(self, target))

        return paths

    def get_path_to_closest_target(self, cm):
        targets = self.get_targets(cm.units)
        paths = []

        for target in targets:
            paths += [(target, path) for path in self._get_paths_to_target(target, cm) if path]

        if paths:
            shortest_distance = len(min(paths, key=lambda x: len(x[1]))[1])
            selected_paths = [path for path in paths if len(path[1]) == shortest_distance]

            selected_paths.sort(key=lambda x: (x[1][0].coordinate.y, x[1][0].coordinate.x))

            selected_path = selected_paths[0][1]
            #print(selected_path)
            if len(selected_path) >= 2:
                return selected_path

    def move(self, coordinate):
        self.coordinate = coordinate

    @property
    def coordinate(self):
        return Coordinate(self.x, self.y)

    @coordinate.setter
    def coordinate(self, coordinate):
        self.x = coordinate.x
        self.y = coordinate.y

    def get_available_adjacent_coordinates(self, cave_map):
        return cave_map.get_available_adjacent_coordinates(self.coordinate)


    def get_targets(self, units):
        return [unit for unit in units if unit.unit_type != self.unit_type and unit.is_alive()]


    def attack(self, unit):
        unit.hp -= self.attack_power

    def is_alive(self):
        return self.hp > 0


class CaveMap(object):
    def __init__(self, cave_data, elf_attack_power):
        self._cave_data = deepcopy(cave_data)
        self._units = []
        self._extract_units(elf_attack_power)

        self._explored_nodes = []
        self._path = []

    def __str__(self):
        cave_data_with_units = deepcopy(self._cave_data)

        for unit in self.units:
            if unit.is_alive():
                cave_data_with_units[unit.y][unit.x] = unit.unit_type

        output = ''
        for row in cave_data_with_units:
            output += ''.join(row)
            output += '\n'
        return output.rstrip()

    def draw(self, field):
        curses.curs_set(0)
        row_index = 0
        for row in self._cave_data:
            output = ''.join(row)

            field.addstr(row_index, 0, output)
            row_index += 1

    def _extract_units(self, elf_attack_power):
        y = 0
        for row in self._cave_data:
            x = 0

            for column in row:
                if column != '#' and column != '.':
                    if column == 'E':
                        self._units.append(Unit(x, y, column, elf_attack_power))
                    else:
                        self._units.append(Unit(x, y, column))
                    self._cave_data[y][x] = '.'

                x += 1
            y += 1

    @property
    def units(self):
        return self._units

    def is_coordinate_open(self, coordinate):
        return self._cave_data[coordinate.y][coordinate.x] == '.'

    def is_coordinate_available(self, coordinate, ignore_unit=None):
        if self.is_coordinate_open(coordinate):
            for unit in self.units:
                if ignore_unit != unit:
                    if unit.is_alive() and unit.coordinate == coordinate:
                        return False
            return True
        return False

    def get_available_adjacent_coordinates(self, coordinate, ignore_unit=None):
        coordinates = []

        for coordinate in [
                Coordinate(coordinate.x, coordinate.y - 1),
                Coordinate(coordinate.x - 1, coordinate.y),
                Coordinate(coordinate.x + 1, coordinate.y),
                Coordinate(coordinate.x, coordinate.y + 1),
        ]:

            if self.is_coordinate_available(coordinate, ignore_unit):
                coordinates.append(coordinate)

        return coordinates

    def get_all_nodes(self):
        nodes = []
        y = 0
        for row in self._cave_data:
            x = 0

            for column in row:
                coordinate = Coordinate(x, y)

                if self.is_coordinate_available(coordinate):
                    nodes.append(Node(coordinate))

                x += 1
            y += 1

        return nodes

    def get_path(self, source, target):
        source_node = Node(source.coordinate)
        target_node = Node(target.coordinate)
        source_node.distance = 0

        queue = deque()
        queue.append(source_node)
        visited = []

        while (len(queue) > 0):
            nodes_on_current_level = []

            while (len(queue) > 0):
                nodes_on_current_level.append(queue.popleft())

            for node in nodes_on_current_level:
                adjecent_nodes = [Node(coordinate) for coordinate in self.get_available_adjacent_coordinates(node.coordinate, target)]

                for adjecent_node in adjecent_nodes:
                    if adjecent_node not in visited:
                        queue.append(adjecent_node)

                        distance = node.distance + 1
                        if distance <= adjecent_node.distance:
                            adjecent_node.distance = distance
                            adjecent_node.parent = node

                        visited.append(adjecent_node)

                    if node == target_node:
                        path = []
                        parent = node.parent
                        while parent:
                            path.append(parent)
                            parent = parent.parent
                        return path

class Node(object):
    def __init__(self, coordinate):
        self.coordinate = coordinate
        self.parent = []
        self.distance = 100000000000000000
        self.done = False

    def __eq__(self, other):
        return self.coordinate == other.coordinate

    def __str__(self):
        return '{}'.format(self.coordinate)

def get_manhattan_distance(p1, p2):
    return abs(p1.x - p2.x) + abs(p1.y - p2.y)

def get_input_from_file(file_name):
    with open(file_name) as f:
        lines = f.readlines()
        return [list(line.rstrip()) for line in lines]

def get_part_one_answer():
    None

def get_part_two_answer():
    None

def check_for_dead_elfs(units):
    for unit in units:
        if unit.unit_type == 'E' and not unit.is_alive():
            return True
    return False


def simulate_battle(cave_data, elf_attack_power):
    if CURSES:
        curses.curs_set(0)
        field = curses.newwin(40, 40, 1, 1)
        curses.start_color()
        curses.use_default_colors()
        for i in range(0, curses.COLORS):
            curses.init_pair(i + 1, i, -1)

    cm = CaveMap(cave_data, elf_attack_power)

    stime = time.time()
    for i in range(1000):

        if CURSES:
            field.clear()
            cm.draw(field)
            curses.curs_set(0)

            for unit in cm.units:
                if unit.is_alive():
                    if unit.unit_type == 'E':
                        field.addstr(unit.y, unit.x, unit.unit_type, curses.color_pair(3))
                    else:
                        field.addstr(unit.y, unit.x, unit.unit_type, curses.color_pair(2))

            field.addstr(33, 0, 'Round {} took {} s'.format(i, time.time() - stime))
            field.refresh()
            #field.getch()
            stime = time.time()
        else:
            print('Round:', i)
            print(cm)

        cm.units.sort(key=lambda unit: (unit.y, unit.x))
        for unit in cm.units:
            if unit.is_alive():
                targets = unit.get_targets(cm.units)
                if targets:
                    target = unit.get_target_in_range(targets)
                    if target:
                        unit.attack(target)
                    else:
                        path = unit.get_path_to_closest_target(cm)
                        if path:
                            unit.coordinate = path[-2].coordinate

                            target = unit.get_target_in_range(targets)
                            if target:
                                unit.attack(target)
                else:
                    hp_sum = 0
                    for unit in cm.units:
                        if unit.is_alive():
                            hp_sum += unit.hp

                    if CURSES:
                        field.clear()
                        cm.draw(field)
                        curses.curs_set(0)
                        for unit in cm.units:
                            if unit.is_alive():
                                if unit.unit_type == 'E':
                                    field.addstr(unit.y, unit.x, unit.unit_type, curses.color_pair(3))
                                else:
                                    field.addstr(unit.y, unit.x, unit.unit_type, curses.color_pair(2))
                        field.addstr(33, 0, 'Round {} took {} s'.format(i, time.time() - stime))
                        field.addstr(34, 0, 'Combat ended after {} rounds'.format(i))
                        field.addstr(35, 0, 'Remaining hit points: {}'.format(hp_sum))
                        field.addstr(36, 0, 'Outcome: {}'.format(i * hp_sum))
                        field.addstr(37, 0, 'Dead elfs: {}'.format(check_for_dead_elfs(cm.units)))
                        field.refresh()
                        field.getch()
                    else:
                        print('Combat ended after {} rounds'.format(i))
                        print(cm)
                        print('Remaining hit points: {}'.format(hp_sum))
                        print(('Outcome: {}'.format(i * hp_sum)))


                    return cm
    return None

def main(stdscr):
    cave_data = get_input_from_file('input.txt')

    simulate_battle(cave_data, 18)

    return 0

    low = 4
    high = 100

    while low < high:
    #for _ in range(10):
        mid = int((low + high) / 2)
        print('low', low)
        print('hig', high)
        print('mid', mid)

        dead_elfs = check_for_dead_elfs(simulate_battle(cave_data, int(mid)).units)
        #print(dead_elfs)
        if dead_elfs:
            low = mid + 1
            #print(low)
        else:
            high = mid

    print('End result:', mid + 1)
    return 0


if __name__ == '__main__':
    if CURSES:
        stime = time.time()
        curses.wrapper(main)
        print('Executed in {} s'.format(time.time() - stime))
    else:
        stime = time.time()
        main(None)
        print('Executed in {} s'.format(time.time() - stime))
