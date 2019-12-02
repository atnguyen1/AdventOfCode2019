#!/usr/bin/env python

import argparse
import math


def fuel_req(mass):
    fr = float(mass) / 3.0
    fr = math.floor(fr)
    fr = fr - 2.0
    return fr


def main(args):
    total_fr = 0
    with open(args.input, 'r') as fh:
        for line in fh:
            mass = int(line)
            total_fr += fuel_req(mass)

    print total_fr


if __name__ == '__main__':
    desc = 'Advent of Code 2019'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--input', type=str, help='Mass')

    args = parser.parse_args()

    main(args)
