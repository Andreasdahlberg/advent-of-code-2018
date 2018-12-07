#!/usr/bin/env python3
# -*- coding: utf-8 -*

from collections import namedtuple
from datetime import datetime

def get_time_from_event(event):
    return event.time


def get_input_from_file(file_name):
    GuardEvent = namedtuple('GuardEvent', ['time', 'text'])

    with open(file_name) as f:
        events = []

        for line in f.readlines():
            date_string = line.split(']')[0][1:]
            text = line.split(']')[1].strip()
            d = datetime.strptime(date_string, '%Y-%m-%d %H:%M')

            guard_event = GuardEvent(d, text)
            events.append(guard_event)

        events.sort(key=get_time_from_event)
        return events


def get_guard_id_with_most_minutes_sleept(guards):
    return max(guards.keys(), key=(lambda k: guards[k]['minutes_sleept']))


def get_guards_with_events(events):
    guards = {}
    guard_id = None

    for event in events:
        if event.text.endswith('begins shift'):
            guard_id = int(event.text.split('#')[1].split()[0])

            if guard_id not in guards:
                guards[guard_id] = {'events': [], 'minutes_sleept': 0}

        if event.text == ('falls asleep'):
            guards[guard_id]['events'].append(event)

        if event.text == ('wakes up'):
            guards[guard_id]['minutes_sleept'] += int((event.time - guards[guard_id]['events'][-1].time).seconds / 60)
            guards[guard_id]['events'].append(event)

    return guards


def get_minute_most_sleept(guard):
    minutes = [0 for y in range(60)]

    start_sleep = None
    for event in guard['events']:
        if event.text == ('falls asleep'):
            start_sleep = event.time

        if event.text == ('wakes up'):
            minutes_sleept = int((event.time - start_sleep).seconds / 60)

            for m in range(start_sleep.minute, start_sleep.minute + minutes_sleept):
                m_index = m % 60

                minutes[m_index] += 1

    return (minutes.index(max(minutes)), max(minutes))


def get_part_one_answer(guards):
    id = get_guard_id_with_most_minutes_sleept(guards)
    minute_most_sleept, _ = get_minute_most_sleept(guards[id])
    return id * minute_most_sleept


def get_part_two_answer(guards):
    minutes_sleep = [(key, get_minute_most_sleept(value)) for key, value in guards.items()]
    guard_who_sleept_most = max(minutes_sleep, key=lambda k: k[1][1])
    return guard_who_sleept_most[0] * guard_who_sleept_most[1][0]


def _main():
    events = get_input_from_file('input.txt')
    guards = get_guards_with_events(events)

    print('Part 1 answer: {}'.format(get_part_one_answer(guards)))
    print('Part 2 answer: {}'.format(get_part_two_answer(guards)))

    return 0


if __name__ == '__main__':
    exit(_main())
