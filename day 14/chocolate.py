#!/usr/bin/env python3
# -*- coding: utf-8 -*

def get_part_one_answer(puzzle_input):
    scoreboard = [3, 7]
    current_recipes = [0, 1]

    while True:
        score_sum = get_new_recipe_sum(scoreboard, current_recipes)
        for c in str(score_sum):
            scoreboard.append(int(c))

        current_recipes[0] = (current_recipes[0] + scoreboard[current_recipes[0]] + 1) % len(scoreboard)
        current_recipes[1] = (current_recipes[1] + scoreboard[current_recipes[1]] + 1) % len(scoreboard)

        if len(scoreboard) > puzzle_input + 10:
            score_sum = ''
            for x in range(puzzle_input, puzzle_input + 10):
                score_sum += str(scoreboard[x])
            return score_sum


def get_part_two_answer(puzzle_input):
    scoreboard = [3, 7]
    current_recipes = [0, 1]

    sequence = str(puzzle_input)
    current_sequence = ''.join([str(c) for c in scoreboard])
    counter = len(scoreboard)

    while True:
        score_sum = get_new_recipe_sum(scoreboard, current_recipes)
        for c in str(score_sum):
            scoreboard.append(int(c))
            counter += 1

            if len(current_sequence) == len(sequence):
                current_sequence = current_sequence[1:] + c
            else:
                current_sequence = current_sequence + c

            if current_sequence == sequence:
                return counter - len(sequence)

        current_recipes[0] = (current_recipes[0] + scoreboard[current_recipes[0]] + 1) % len(scoreboard)
        current_recipes[1] = (current_recipes[1] + scoreboard[current_recipes[1]] + 1) % len(scoreboard)


def get_new_recipe_sum(scoreboard, current_recipes):
    return scoreboard[current_recipes[0]] + scoreboard[current_recipes[1]]


def _main():

    print('Part 1 answer: {}'.format(get_part_one_answer(360781)))
    print('Part 2 answer: {}'.format(get_part_two_answer(360781)))

    return 0


if __name__ == '__main__':
    exit(_main())
