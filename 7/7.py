#!/usr/bin/env python

from __future__ import print_function

import argparse
import sys


def permutation(lst):
    # If lst is empty then there are no permutations
    if len(lst) == 0:
        return []

    # If there is only one element in lst then, only
    # one permuatation is possible
    if len(lst) == 1:
        return [lst]

    l1 = []   # empty list that will store current permutation

    # Iterate the input(lst) and calculate the permutation
    for i in range(len(lst)):
        m = lst[i]
        remLst = lst[:i] + lst[i + 1:]
        # Generating all permutations where m is first
        # element
        for p in permutation(remLst):
            l1.append([m] + p)
    return l1


class int_computer:
    def __init__(self, amplifier_id, phase_setting, data_input, data):
        self.amplifier_id = amplifier_id
        self.data = data
        self.phase_setting = phase_setting
        self.data_input = data_input
        self.output = None

    def get_output(self):
        return self.output

    def run(self):

        set_phase = False
        system_input = self.data_input
        system_phase = self.phase_setting
        data = self.data

        opcode = 0
        current_instruction = 0
        registers = 0
        program_output = None

        while opcode != 99:
            jump = False
            init_instruction = str(data[current_instruction])
            if len(init_instruction) >= 2:
                opcode = int(init_instruction[-2:])
                parameter_modes = init_instruction[:-2]   # Remove opcode portions
                parameter_modes = parameter_modes[::-1]   # Reverse
                parameter_modes = list(parameter_modes)
                parameter_modes = [int(x) for x in parameter_modes]
                if len(parameter_modes) == 0:
                    parameter_modes = [0]
            else:
                opcode = int(init_instruction)
                parameter_modes = [0]

            # print(init_instruction)
            # print(opcode)
            # print(parameter_modes)

            if opcode == 99:
                break
            if opcode == 1:
                while len(parameter_modes) < 3:
                    parameter_modes.append(0)
                # print(current_instruction, opcode, data[current_instruction:current_instruction + 4])
                if parameter_modes[0] == 0:
                    add1 = data[current_instruction + 1]
                    add1 = data[add1]
                elif parameter_modes[0] == 1:
                    add1 = data[current_instruction + 1]

                if parameter_modes[1] == 0:
                    add2 = data[current_instruction + 2]
                    add2 = data[add2]
                elif parameter_modes[1] == 1:
                    add2 = data[current_instruction + 2]

                # print('Adding', add1, add2)

                # Outputs never put immediate mode
                if parameter_modes[2] == 0:
                    output_pos = data[current_instruction + 3]
                    data[output_pos] = add1 + add2

                registers = 4
                # print(current_instruction, opcode, data[current_instruction:current_instruction + 4])
            if opcode == 2:
                while len(parameter_modes) < 3:
                    parameter_modes.append(0)
                # print(current_instruction, opcode, data[current_instruction:current_instruction + 4])
                if parameter_modes[0] == 0:
                    mul1 = data[current_instruction + 1]
                    mul1 = data[mul1]
                elif parameter_modes[0] == 1:
                    mul1 = data[current_instruction + 1]

                if parameter_modes[1] == 0:
                    mul2 = data[current_instruction + 2]
                    mul2 = data[mul2]
                elif parameter_modes[1] == 1:
                    mul2 = data[current_instruction + 2]

                # print('Multiplying', mul1, mul2)

                if parameter_modes[2] == 0:
                    output_pos = data[current_instruction + 3]
                    data[output_pos] = mul1 * mul2
                registers = 4
                # print(current_instruction, opcode, data[current_instruction:current_instruction + 4])
            if opcode == 3:
                # Single parameter
                # Opcode 3 is always in position mode
                # print(current_instruction, opcode, data[current_instruction:current_instruction + 2])
                output = data[current_instruction + 1]
                # original_val = data[output]

                # First input set phase, second input set input from previous int_code
                if not set_phase:
                    data[output] = system_phase
                    set_phase = True
                else:
                    data[output] = system_input
                registers = 2

                # print('Operation, place', system_input, 'at location', output, 'Replaceing', original_val)
            if opcode == 4:
                # Single parameter
                # print(current_instruction, opcode, data[current_instruction:current_instruction + 2])
                if parameter_modes[0] == 0:
                    # Address Mode
                    output = data[current_instruction + 1]
                    output = data[output]
                else:
                    # Immediate mode
                    output = data[current_instruction + 1]
                # output = data[current_instruction + 1]
                # print('Output:', output)
                program_output = output
                registers = 2
            if opcode == 5:
                while len(parameter_modes) < 2:
                    parameter_modes.append(0)
                # print(current_instruction, opcode, data[current_instruction:current_instruction + 3])
                if parameter_modes[0] == 0:
                    lookup = data[current_instruction + 1]
                    lookup = data[lookup]
                elif parameter_modes[0] == 1:
                    lookup = data[current_instruction + 1]

                if parameter_modes[1] == 0:
                    jump_add = data[current_instruction + 2]
                    jump_add = data[jump_add]
                elif parameter_modes[1] == 1:
                    jump_add = data[current_instruction + 2]

                if lookup > 0:
                    # print('Jump if True', lookup, 'Jumpping to', jump_add)
                    # print('Value at Jump Address', data[current_instruction + 2])
                    current_instruction = jump_add
                    jump = True
                else:
                    registers = 3
            if opcode == 6:
                while len(parameter_modes) < 2:
                    parameter_modes.append(0)
                # print(current_instruction, opcode, data[current_instruction:current_instruction + 3])
                if parameter_modes[0] == 0:
                    lookup = data[current_instruction + 1]
                    lookup = data[lookup]
                elif parameter_modes[0] == 1:
                    lookup = data[current_instruction + 1]

                if parameter_modes[1] == 0:
                    jump_add = data[current_instruction + 2]
                    jump_add = data[jump_add]
                elif parameter_modes[1] == 1:
                    jump_add = data[current_instruction + 2]

                # print('Jump if False', lookup, 'Jumping to ', jump_add)
                if lookup == 0:
                    current_instruction = jump_add
                    jump = True
                    # print('Jumping to ', current_instruction + 2, 'Replacing', data[current_instruction + 2])
                else:
                    registers = 3

            if opcode == 7:
                while len(parameter_modes) < 3:
                    parameter_modes.append(0)
                # print(current_instruction, opcode, data[current_instruction:current_instruction + 3])
                if parameter_modes[0] == 0:
                    arg1 = data[current_instruction + 1]
                    arg1 = data[arg1]
                elif parameter_modes[0] == 1:
                    arg1 = data[current_instruction + 1]

                if parameter_modes[1] == 0:
                    arg2 = data[current_instruction + 2]
                    arg2 = data[arg2]
                elif parameter_modes[1] == 1:
                    arg2 = data[current_instruction + 2]

                if parameter_modes[2] == 0:
                    arg3 = data[current_instruction + 3]
                else:
                    print('opcode 7 failed to write Arg 3')

                if arg1 < arg2:
                    data[arg3] = 1
                else:
                    data[arg3] = 0

                registers = 4
            if opcode == 8:
                # Parameter mode implementation is wrong, 1 level too deep.

                while len(parameter_modes) < 3:
                    parameter_modes.append(0)
                # print(current_instruction, opcode, data[current_instruction:current_instruction + 4])
                if parameter_modes[0] == 0:
                    arg1 = data[current_instruction + 1]
                    arg1 = data[arg1]
                elif parameter_modes[0] == 1:
                    arg1 = data[current_instruction + 1]

                if parameter_modes[1] == 0:
                    arg2 = data[current_instruction + 2]
                    arg2 = data[arg2]
                elif parameter_modes[1] == 1:
                    arg2 = data[current_instruction + 2]

                if parameter_modes[2] == 0:
                    arg3 = data[current_instruction + 3]
                else:
                    print('opcode 8 failed to write Arg 3')

                # print('ARGS', arg1, arg2, arg3)
                if arg1 == arg2:
                    data[arg3] = 1
                else:
                    data[arg3] = 0

                registers = 4

            # print('Data', data)
            if not jump:
                current_instruction += registers

        self.output = program_output


def main(args):
    # Main
    data = list()
    with open(args.input, 'r') as fh:
        for line in fh:
            line = line.rstrip().split(',')
            data += line

    data = [int(x) for x in data]

    phase_settings = [0, 1, 2, 3, 4]
    phase_permutations = list()

    for p in permutation(phase_settings):
        phase_permutations.append(p)

    # print(len(phase_permutations))    # 120

    run_data = dict()

    for z, p in enumerate(phase_permutations):
        a_phase = p[0]
        b_phase = p[1]
        c_phase = p[2]
        d_phase = p[3]
        e_phase = p[4]

        a = int_computer('A', a_phase, 0, data)
        a.run()
        a_output = a.get_output()

        b = int_computer('B', b_phase, a_output, data)
        b.run()
        b_output = b.get_output()

        c = int_computer('C', c_phase, b_output, data)
        c.run()
        c_output = c.get_output()

        d = int_computer('D', d_phase, c_output, data)
        d.run()
        d_output = d.get_output()

        e = int_computer('E', e_phase, d_output, data)
        e.run()
        e_output = e.get_output()

        if e_output not in run_data:
            run_data[e_output] = [z]
        else:
            run_data[e_output].append(z)

    print('Thrust Values')
    srd = sorted(run_data.keys())
    max_thrust = srd[-1]
    print(srd)
    print('Max Thrust', max_thrust)
    print('Phase Settings:')
    print(run_data[max_thrust])
    print(phase_permutations[run_data[max_thrust][0]])


if __name__ == '__main__':
    desc = 'Advent of Code 2019'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--input', type=str, help='Mass')

    args = parser.parse_args()

    main(args)
