#!/usr/bin/env python

from __future__ import print_function

import argparse
import math
from collections import Counter
import sys


def main(args):
    data = list()
    with open(args.input, 'r') as fh:
        for line in fh:
            line = line.rstrip().split(',')
            data += line

    data = [int(x) for x in data]

    system_id = 1
    system_input = system_id

    opcode = 0
    current_instruction = 0
    registers = 0

    # data = [1002, 4, 3, 4, 33]

    while opcode != 99:
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

            if parameter_modes[2] == 0:
                output_pos = data[current_instruction + 3]
                data[output_pos] = mul1 * mul2
            registers = 4
            # print(current_instruction, opcode, data[current_instruction:current_instruction + 4])
        if opcode == 3:
            # Single parameter
            # Doesn't matter as we are writing input to whatever is there in address
            # print(current_instruction, opcode, data[current_instruction:current_instruction + 2])
            if parameter_modes[0] == 0:
                # Address Mode
                output = data[current_instruction + 1]
                output = data[output]
            else:
                # Immediate mode
                output = data[current_instruction + 1]

            # output = data[current_instruction + 1]
            data[output] = system_input
            registers = 2
        if opcode == 4:
            # Single parameter
            if parameter_modes[0] == 0:
                # Address Mode
                output = data[current_instruction + 1]
                output = data[output]
            else:
                # Immediate mode
                output = data[current_instruction + 1]
            # print(current_instruction, opcode, data[current_instruction:current_instruction + 2])
            print('Output:', output)
            registers = 2
        current_instruction += registers

    # print(data)


if __name__ == '__main__':
    desc = 'Advent of Code 2019'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--input', type=str, help='Mass')

    args = parser.parse_args()

    main(args)
