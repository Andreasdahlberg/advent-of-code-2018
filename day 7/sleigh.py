#!/usr/bin/env python3
# -*- coding: utf-8 -*

import re

def get_input_from_file(file_name):
    steps = {}

    with open(file_name) as f:
        pattern = re.compile('step\s(\S)', re.IGNORECASE)
        lines = f.readlines()

        for line in lines:
            pre, step_id = pattern.findall(line)
            if step_id not in steps:
                steps[step_id] = [pre]
            else:
                steps[step_id].append(pre)
    return steps


def is_pre_completed(completed_steps, pre):
    for p in pre:
        if p not in completed_steps:
            return False
    return True


def get_available_steps(completed_steps, steps):
    result = find_starting_steps(completed_steps, steps)

    for step_id in steps:
        if step_id not in completed_steps and is_pre_completed(completed_steps, steps[step_id]):
            result.append(step_id)

    result.sort()
    return result


def get_available_step(completed_steps, steps):
    result = get_available_steps(completed_steps, steps)
    if result:
        return result[0]
    else:
        return None


def find_starting_steps(completed_steps, steps):
    res = []

    for key in steps:
        pre = steps[key]

        for p in pre:
            if not p in steps and p not in res and p not in completed_steps:
                res.append(p)
    return res


def get_step_time(step_id):
    return ord(step_id) - 4


def get_part_one_answer(data):
    completed_steps = []

    while True:
        next_step = get_available_step(completed_steps, data)
        if next_step:
            completed_steps.append(next_step)
        else:
            break

    return ''.join(completed_steps)


def get_part_two_answer(data):
    completed_steps = []
    steps_in_progress = []
    workers = [{'step': None, 'time': 0} for y in range(5)]

    t = 0

    pause = False

    while True:
        pause = False
        for i in range(0, len(workers)):
            if workers[i]['time'] == 0:

                if workers[i]['step']:
                    print('T{} Worker {} completed step {}'.format(t, i, workers[i]['step']))
                    completed_steps.append(workers[i]['step'])
                    workers[i]['step'] = None
                    pause = True
                    break

                next_steps = get_available_steps(completed_steps, data)

                if not next_steps:
                    return t

                for next_step in next_steps:
                    if next_step not in steps_in_progress:
                        print('T{} Worker {} started step {}'.format(t, i, next_step))
                        workers[i]['step'] = next_step
                        workers[i]['time'] = get_step_time(next_step)
                        steps_in_progress.append(next_step)
                        break
        if not pause:
            t += 1
            for i in range(0, len(workers)):
                if workers[i]['time'] > 0:
                    workers[i]['time'] -= 1

    return t

def _main():
    data = get_input_from_file('input.txt')


    print('Part 1 answer: {}'.format(get_part_one_answer(data)))
    print('Part 2 answer: {}'.format(get_part_two_answer(data)))

    return 0


if __name__ == '__main__':
    exit(_main())
