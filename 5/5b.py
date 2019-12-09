#!/usr/bin/env python

from __future__ import print_function

import argparse
import sys


def main(args):
    data = list()
    with open(args.input, 'r') as fh:
        for line in fh:
            line = line.rstrip().split(',')
            data += line

    data = [int(x) for x in data]

    system_id = 5
    system_input = system_id

    opcode = 0
    current_instruction = 0
    registers = 0

    # data = [1002, 4, 3, 4, 33]
    # data = [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9]
    # data = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]   # 0 if != 8, 1 if == 8 pos mode
    # data = [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]   # 1 if < 8, else 0  pos mode
    # data = [3, 3, 1108, -1, 8, 3, 4, 3, 99]         # 1 if == 8 else 0, imm mode

    # Jump Tets

    # data = [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9]
    # data =[3,3,1105,-1,9,1101,0,0,12,4,12,99,1]

    # data = [3,21,1008,21,8,20,1005,20,22,107,8,21,20,1006,20,31,
    #         1106,0,36,98,0,0,1002,21,125,20,4,20,1105,1,46,104,
    #         999,1105,1,46,1101,1000,1,20,4,20,1105,1,46,98,99]

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
            original_val = data[output]
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
            print('Output:', output)
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

    # print(data)


if __name__ == '__main__':
    desc = 'Advent of Code 2019'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--input', type=str, help='Mass')

    args = parser.parse_args()

    main(args)
