#!/usr/bin/env python

from __future__ import print_function

import argparse
import math
from collections import Counter
import sys


def main(args):
    # 264793-803935
    minimum = 264793
    maximum = 803935

    passwords = range(minimum, maximum)
    valid_passwords = list()

    for ps in passwords:
        p = str(ps)
        if int(p[0]) <= int(p[1]):
            if int(p[1]) <= int(p[2]):
                if int(p[2]) <= int(p[3]):
                    if int(p[3]) <= int(p[4]):
                        if int(p[4]) <= int(p[5]):
                            data = Counter(p)
                            valid = False

                            for key in data:
                                if data[key] >= 2:
                                    valid = True
                            if valid:
                                valid_passwords.append(ps)

    print(len(valid_passwords))
    for v in valid_passwords:
        print(v)


if __name__ == '__main__':
    desc = 'Advent of Code 2019'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--input', type=str, help='Mass')

    args = parser.parse_args()

    main(args)
