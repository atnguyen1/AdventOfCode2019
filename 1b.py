#!/usr/bin/env python

from __future__ import print_function

import argparse
import math
import sys


def fuel_req(mass):
    fr = float(mass) / 3.0
    fr = math.floor(fr)
    fr = fr - 2.0
    return fr


def main(args):
    total_module_mass = []
    if args.mass:
        total_module_mass.append(float(args.mass))
    if args.input:
        with open(args.input, 'r') as fh:
            for line in fh:
                line = line.rstrip()
                total_module_mass.append(line)

    all_module_fuel = 0
    for module in total_module_mass:
        fr = fuel_req(module)
        print('Module Added Fuel', fr)
        added_fuel = fr
        additional_fuel = [fr]
        while added_fuel > 0:
            added_fuel = fuel_req(added_fuel)
            if added_fuel > 0:
                additional_fuel.append(added_fuel)

        print(additional_fuel)
        print(sum(additional_fuel))
        all_module_fuel += sum(additional_fuel)

    print('Total Module Fuel Req:', all_module_fuel)


if __name__ == '__main__':
    desc = 'Advent of Code 2019'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--input', type=str, help='Mass')
    parser.add_argument('--mass', type=str, help='Mass')

    args = parser.parse_args()

    main(args)
