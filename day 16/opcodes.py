#!/usr/bin/env python3
# -*- coding: utf-8 -*

from copy import deepcopy
from collections import namedtuple
import re

Instruction = namedtuple('Instruction', ['opcode', 'a',  'b', 'c'])
Sample = namedtuple('Sample', ['before', 'instruction',  'after'])

def get_samples_from_file(file_name):
    with open(file_name) as f:
        pattern = re.compile('(\d+)')

        data = []
        samples = []
        lines = f.readlines()
        for line in lines:
            if line.rstrip():
                values = [int(value) for value in pattern.findall(line.rstrip())]
                if line[0].isdigit():
                    instruction = Instruction(*values)
                    data.append(instruction)
                else:
                    data.append(values)
            else:
                sample = Sample(*data)
                samples.append(sample)
                data = []
        return samples


def get_program_from_file(file_name):
    instructions = []

    with open(file_name) as f:
        lines = f.readlines()
        for line in lines:
            instruction = Instruction(*[int(value) for value in line.rstrip().split(' ')])
            instructions.append(instruction)
        return instructions


def addr(registers, instruction):
    registers[instruction.c] = registers[instruction.a] + registers[instruction.b]


def addi(registers, instruction):
    registers[instruction.c] = registers[instruction.a] + instruction.b


def mulr(registers, instruction):
    registers[instruction.c] = registers[instruction.a] * registers[instruction.b]


def muli(registers, instruction):
    registers[instruction.c] = registers[instruction.a] * instruction.b


def banr(registers, instruction):
    registers[instruction.c] = registers[instruction.a] & registers[instruction.b]


def bani(registers, instruction):
    registers[instruction.c] = registers[instruction.a] & instruction.b


def borr(registers, instruction):
    registers[instruction.c] = registers[instruction.a] | registers[instruction.b]


def bori(registers, instruction):
    registers[instruction.c] = registers[instruction.a] | instruction.b


def setr(registers, instruction):
    registers[instruction.c] = registers[instruction.a]


def seti(registers, instruction):
    registers[instruction.c] = instruction.a


def gtir(registers, instruction):
    registers[instruction.c] = int(instruction.a > registers[instruction.b])


def gtri(registers, instruction):
    registers[instruction.c] = int(registers[instruction.a] > instruction.b)


def gtrr(registers, instruction):
    registers[instruction.c] = int(registers[instruction.a] > registers[instruction.b])


def eqir(registers, instruction):
    registers[instruction.c] = int(instruction.a == registers[instruction.b])


def eqri(registers, instruction):
    registers[instruction.c] = int(registers[instruction.a] == instruction.b)


def eqrr(registers, instruction):
    registers[instruction.c] = int(registers[instruction.a] == registers[instruction.b])


def decode(opcode, decoder):
    return decoder[opcode]


def execute(registers, instruction, decoder):
    func = decode(instruction.opcode, decoder)
    func(registers, instruction)


def run_program(decoder):
    program = get_program_from_file('input_program.txt')
    registers = [0, 0, 0, 0]
    for instruction in program:
        execute(registers, instruction, decoder)
    return registers


def get_decoder_from_samples(samples):
    DEFAULT_OPCODES = {
        0: addr,
        1: addi,
        2: mulr,
        3: muli,
        4: banr,
        5: bani,
        6: borr,
        7: bori,
        8: setr,
        9: seti,
        10: gtir,
        11: gtri,
        12: gtrr,
        13: eqir,
        14: eqri,
        15: eqrr
    }

    result = 0
    possible_op = {}

    for sample in samples:
        match_counter = 0
        for opcode in range(16):
            instruction = sample.instruction
            test_instruction = Instruction(opcode, instruction.a, instruction.b, instruction.c)

            registers = deepcopy(sample.before)
            execute(registers, test_instruction, DEFAULT_OPCODES)

            if registers == sample.after:
                func = decode(opcode, DEFAULT_OPCODES)

                if func not in possible_op:
                    possible_op[func] = [instruction.opcode]
                else:
                    if instruction.opcode not in possible_op[func]:
                        possible_op[func].append(instruction.opcode)

                match_counter += 1
        if match_counter >= 3:
            result += 1

    while True:
        used_opcodes = []
        for func, opcodes in sorted(possible_op.items(), key=lambda kv: len(kv[1])):
            for used_opcode in used_opcodes:
                opcodes = [opcode for opcode in opcodes if opcode not in used_opcodes]

            if (len(opcodes) == 1):
                used_opcodes += opcodes
                possible_op[func] = opcodes

        if (len(used_opcodes) == 16):
            break


    decoder = {}
    for func, opcode in possible_op.items():
        decoder[opcode[0]] = func

    return decoder, result


def _main():
    samples = get_samples_from_file('input_samples.txt')
    decoder, result = get_decoder_from_samples(samples)
    registers = run_program(decoder)

    print('Part 1 answer: {}'.format(result))
    print('Part 2 answer: {}'.format(registers[0]))

    return 0


if __name__ == '__main__':
    exit(_main())
