from collections import namedtuple
import copy

Coordinate = namedtuple('Coordinate', ['x', 'y'])

OPEN = '.'
TREE = '|'
LUMBERYARD = '#'


def get_map_from_file(file_name):

    with open(file_name) as f:
        lines = f.readlines()

        y_max = 0
        for line in lines:
            x_max = 0
            for acre in line.rstrip():
                x_max += 1
            y_max += 1
    #print('x: {}, y: {}'.format(x_max, y_max))
    area_map = [[ '.' for x in range(x_max)] for y in range(y_max)]

    y = 0
    for line in lines:
        x = 0
        for acre in line.rstrip():
            area_map[y][x] = acre
            x += 1
        y += 1

    return area_map


class LumberCollectionArea(object):
    def __init__(self, area_map):
        self._area_map = area_map

    def _count_acres(self, acre_types):
        count = 0
        for row in self._area_map:
            for acre in row:
                if acre in acre_types:
                    count += 1
        return count

    def _set_acre(self, coordinate, acre_type):
        self._area_map[coordinate.y][coordinate.x] = acre_type

    def _get_acre(self, coordinate, area_map):
        try:
            return area_map[coordinate.y][coordinate.x]
        except IndexError:
            return None

    def _get_adjecent_acres(self, coordinate):
        adjecent_acres = []

        if coordinate.x > 0:
            x_min = coordinate.x - 1
        else:
            x_min = 0

        if coordinate.y > 0:
            y_min = coordinate.y - 1
        else:
            y_min = 0

        x_max = coordinate.x + 1
        y_max = coordinate.y + 1

        for y in range(y_min, y_max + 1):
            for x in range(x_min, x_max + 1):
                c = Coordinate(x, y)

                if c != coordinate:
                    adjecent_acres.append(self._get_acre(c, self._prev_area_map))

        return adjecent_acres

    def _update_open_acre(self, coordinate):
        #print('_update_open_acre', coordinate)
        adjecent_acres = self._get_adjecent_acres(coordinate)
        number_of_adjecent_trees = adjecent_acres.count(TREE)
        if number_of_adjecent_trees >= 3:
            self._set_acre(coordinate, TREE)

    def _update_tree_acre(self, coordinate):
        #print('_update_tree_acre', coordinate)
        adjecent_acres = self._get_adjecent_acres(coordinate)
        number_of_adjecent_lumberyards = adjecent_acres.count(LUMBERYARD)
        if number_of_adjecent_lumberyards >= 3:
            self._set_acre(coordinate, LUMBERYARD)

    def _update_lumberyard_acre(self, coordinate):
        #print('_update_lumberyard_acre', coordinate)
        adjecent_acres = self._get_adjecent_acres(coordinate)
        number_of_adjecent_lumberyards = adjecent_acres.count(LUMBERYARD)
        number_of_adjecent_trees = adjecent_acres.count(TREE)
        if number_of_adjecent_lumberyards == 0 or number_of_adjecent_trees == 0:
            self._set_acre(coordinate, OPEN)

    def _update(self):
        update_acre = {
            OPEN: self._update_open_acre,
            TREE: self._update_tree_acre,
            LUMBERYARD: self._update_lumberyard_acre,
        }

        self._prev_area_map = copy.deepcopy(self._area_map)
        y = 0
        for row in self._area_map:
            x = 0
            for acre in row:
                update_acre[acre](Coordinate(x=x, y=y))
                x += 1
            y += 1

    def draw(self):
        for row in self._area_map:
            print(''.join(row))
        print()

    def run(self, duration):
        #self.draw()
        for minute in range(duration):
            self._update()
            #self.draw()

    @property
    def number_of_trees(self):
        return self._count_acres([TREE])

    @property
    def number_of_lumberyards(self):
        return self._count_acres([LUMBERYARD])

    @property
    def resource_value(self):
        return self.number_of_trees * self.number_of_lumberyards


def _main():
    pattern = [
        202124,
        198660,
        202070,
        200690,
        206581,
        206746,
        213624,
        214375,
        218544,
        217408,
        222534,
        222662,
        226914,
        226914,
        229680,
        226135,
        227160,
        225164,
        224237,
        215380,
        210000,
        205114,
        204336,
        196350,
        198990,
        197208,
        200772,
        199398
    ]

    area_map = get_map_from_file('input.txt')
    lumber_collection_area = LumberCollectionArea(area_map)
    lumber_collection_area.run(10)

    print('Part 1 answer: {}'.format(lumber_collection_area.resource_value))
    print('Part 2 answer: {}'.format(pattern[1000000000  % len(pattern)]))

    return 0


if __name__ == '__main__':
    exit(_main())
