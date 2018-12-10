#!/usr/bin/env python3
# -*- coding: utf-8 -*

import re
from blist import blist

def get_answer(number_of_players, number_of_marbles):
    scores = [0 for i in range(number_of_players)]

    circle = blist([0])
    current_marble_index = 0
    marble_value = 1

    while marble_value < number_of_marbles + 1:
        if marble_value % 23 == 0:
            player_index = marble_value % number_of_players
            scores[player_index] += marble_value

            tmp_i = (len(circle) + current_marble_index - 7) % len(circle)
            scores[player_index] += circle[tmp_i]
            del circle[tmp_i]
            current_marble_index = tmp_i

        else:
            if len(circle) > 0:
                if (current_marble_index + 2) == len(circle):
                    i = current_marble_index + 2
                else:
                    i = (current_marble_index + 2) % (len(circle))
            else:
                i = 1

            circle.insert(i, marble_value)
            current_marble_index = i

        marble_value += 1

    scores.sort()
    return scores[-1]


def _main():
    print('Part 1 answer: {}'.format(get_answer(418, 71339)))
    print('Part 2 answer: {}'.format(get_answer(418, 7133900)))

    return 0


if __name__ == '__main__':
    exit(_main())
