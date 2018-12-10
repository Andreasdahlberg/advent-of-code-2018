#!/usr/bin/env python3
# -*- coding: utf-8 -*

from collections import deque
import io
import struct


class Node(object):
    def __init__(self):
        self._children = []
        self._metadata = []
        self.number_of_children = 0
        self.number_of_metadata_entries = 0

    def add_child(self, child):
        self._children.append(child)

    def add_metadata(self, metadata):
        self._metadata.append(metadata)

    def get_value(self):
        value = 0

        if len(self._children) == 0:
            value += sum(self._metadata)
        else:
            for entry in self._metadata:
                if entry <= len(self._children):
                    child_index = len(self._children) - entry
                    value += self._children[child_index].get_value()
        return value


def get_input_from_file(file_name):
    with open(file_name) as f:
        data = f.read().rstrip()
        return [int(value) for value in data.split()]


def get_part_one_answer(nodes):
    metadata_sum = 0
    for node in nodes:
        metadata_sum += sum(node._metadata)
    return metadata_sum


def get_part_two_answer(nodes):
    return nodes[0].get_value()


def fill_node(stream, stack, nodes):
    node = stack[-1]

    if node.number_of_metadata_entries == 0:
        header = stream.read(2)
        node.number_of_children, node.number_of_metadata_entries = struct.unpack('>BB', header)

    if len(node._children) == node.number_of_children:
        for _ in range(node.number_of_metadata_entries):
            metadata = stream.read(1)
            node.add_metadata(struct.unpack('>B', metadata)[0])
        stack.pop()
    else:
        for _ in range(node.number_of_children):
            child_node = Node()
            node.add_child(child_node)
            nodes.append(child_node)
            stack.append(child_node)


def _main():
    node_data = get_input_from_file('input.txt')
    stream = io.BytesIO(bytes(node_data))

    stack = deque()
    root_node = Node()

    stack.append(root_node)
    nodes = [root_node]

    while len(stack) > 0:
        fill_node(stream, stack, nodes)

    print('Part 1 answer: {}'.format(get_part_one_answer(nodes)))
    print('Part 2 answer: {}'.format(get_part_two_answer(nodes)))

    return 0


if __name__ == '__main__':
    exit(_main())
