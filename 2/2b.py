#!/usr/bin/env python

from __future__ import print_function

import argparse
import math
import sys


def main(args):
    data_init = []
    with open(args.input, 'r') as fh:
        for line in fh:
            line = line.rstrip().split(',')
            data_init = line

    # Problem setup
    for noun in range(0, 100):
        for verb in range(0, 100):
            data = [int(x) for x in data_init]
            data[1] = noun
            data[2] = verb

            try:
                opcode = 0
                current_instruction = 0

                while opcode != 99:
                    opcode = data[current_instruction]
                    if opcode == 99:
                        break
                    if opcode == 1:
                        add1 = data[current_instruction + 1]
                        add2 = data[current_instruction + 2]
                        output_pos = data[current_instruction + 3]
                        data[output_pos] = data[add1] + data[add2]
                    if opcode == 2:
                        mul1 = data[current_instruction + 1]
                        mul2 = data[current_instruction + 2]
                        output_pos = data[current_instruction + 3]
                        data[output_pos] = data[mul1] * data[mul2]
                    current_instruction += 4
                    if current_instruction > len(data):
                        break
                if data[0] == 19690720:
                    print('Found')
                    print(noun, verb)
                    print(100 * noun + verb)
                    print(data)
                    sys.exit()
            except IndexError:
                continue

    print(data)


if __name__ == '__main__':
    desc = 'Advent of Code 2019'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--input', type=str, help='Mass')

    args = parser.parse_args()

    main(args)
