from collections import namedtuple

NUMBER_OF_REGISTERS = 6

Instruction = namedtuple('Instruction', ['opcode', 'a',  'b', 'c'])


def get_program_from_file(file_name):
    instructions = []

    with open(file_name) as f:
        lines = f.readlines()

        intstruction_pointer_register = int(lines[0].split(' ')[-1])

        for line in lines[1:]:
            if line.rstrip() and line[0] != '#':
                instruction_components = line.split(' ')
                instruction = Instruction(
                    instruction_components[0],
                    int(instruction_components[1]),
                    int(instruction_components[2]),
                    int(instruction_components[3])
                )
                instructions.append(instruction)
        return intstruction_pointer_register, instructions


class Executable(object):
    def __init__(self, instruction_set, instructions):
        self._isa = instruction_set
        self._instructions = instructions

    def run(self):
        while self._isa.instruction_pointer < len(self._instructions):
            instruction = self._instructions[self._isa.instruction_pointer]
            self._isa.execute(instruction)
            self._isa.instruction_pointer += 1

        self._isa.instruction_pointer -= 1
        return 0


class InstructionSet(object):
    def __init__(self, number_of_registers=NUMBER_OF_REGISTERS, intstruction_pointer_register=0):
        self._registers = [0 for _ in range(number_of_registers)]
        self._intstruction_pointer_register = intstruction_pointer_register
        self._number_of_registers = number_of_registers

    def _addr(self, instruction):
        self._registers[instruction.c] = self._registers[instruction.a] + self._registers[instruction.b]

    def _addi(self, instruction):
        self._registers[instruction.c] = self._registers[instruction.a] + instruction.b

    def _mulr(self, instruction):
        self._registers[instruction.c] = self._registers[instruction.a] * self._registers[instruction.b]

    def _muli(self, instruction):
        self._registers[instruction.c] = self._registers[instruction.a] * instruction.b

    def _banr(self, instruction):
        self._registers[instruction.c] = self._registers[instruction.a] & self._registers[instruction.b]

    def _bani(self, instruction):
        self._registers[instruction.c] = self._registers[instruction.a] & instruction.b

    def _borr(self, instruction):
        self._registers[instruction.c] = self._registers[instruction.a] | self._registers[instruction.b]

    def _bori(self, instruction):
        self._registers[instruction.c] = self._registers[instruction.a] | instruction.b

    def _setr(self, instruction):
        self._registers[instruction.c] = self._registers[instruction.a]

    def _seti(self, instruction):
        self._registers[instruction.c] = instruction.a

    def _gtir(self, instruction):
        self._registers[instruction.c] = int(instruction.a > self._registers[instruction.b])

    def _gtri(self, instruction):
        self._registers[instruction.c] = int(self._registers[instruction.a] > instruction.b)

    def _gtrr(self, instruction):
        self._registers[instruction.c] = int(self._registers[instruction.a] > self._registers[instruction.b])

    def _eqir(self, instruction):
        self._registers[instruction.c] = int(instruction.a == self._registers[instruction.b])

    def _eqri(self, instruction):
        self._registers[instruction.c] = int(self._registers[instruction.a] == instruction.b)

    def _eqrr(self, instruction):
        self._registers[instruction.c] = int(self._registers[instruction.a] == self._registers[instruction.b])

    def _decode(self, instruction):
        return getattr(self, '_' + instruction.opcode)

    def execute(self, instruction):
        func = self._decode(instruction)
        #print('{:<4} [{:<4} {:<4} {:<8} {:<4} {:<4} {:<8}]'.format(self.instruction_pointer, *self._registers), instruction)
        func(instruction)

    @property
    def number_of_registers(self):
        return self._number_of_registers

    @property
    def instruction_pointer(self):
        return self._registers[self._intstruction_pointer_register]

    @instruction_pointer.setter
    def instruction_pointer(self, instruction_pointer):
        self._registers[self._intstruction_pointer_register] = instruction_pointer

    def get_register_value(self, register):
        return self._registers[register]

    def  set_register_value(self, register, value):
        self._registers[register] = value


def _main():
    intstruction_pointer_register, instructions = get_program_from_file('input.txt')

    isa = InstructionSet(intstruction_pointer_register=intstruction_pointer_register)
    exe = Executable(isa, instructions)
    exe.run()
    print('Part 1 answer: {}'.format(isa.get_register_value(0)))

    # Part 2 will never finish, see c-program for solution.
    #isa = InstructionSet(intstruction_pointer_register=intstruction_pointer_register)
    #isa.set_register_value(0, 1)
    #exe = Executable(isa, instructions)
    #exe.run()
    #print('Part 2 answer: {}'.format(isa.get_register_value(0)))

    return 0


if __name__ == '__main__':
    exit(_main())
