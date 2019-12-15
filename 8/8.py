#!/usr/bin/env python

from __future__ import print_function

import argparse
import sys

from collections import Counter


def grab_layers(input, width):
    for i in xrange(0, len(input), width):
        yield input[i:i + width]


def format_columns(input, height):
    for i in xrange(0, len(input), height):
        yield input[i:i + height]


def main(args):
    data = list()
    with open(args.input, 'r') as fh:
        for line in fh:
            line = line.rstrip()
            data += line

    img_height = 6
    img_width = 25

    layers = grab_layers(data, img_height * img_width)

    layer_info = dict()

    for z, l in enumerate(layers):
        counts = Counter(l)
        # Fix counts
        if '0' not in counts:
            counts['0'] = 0
        if '1' not in counts:
            counts['0'] = 0
        if '2' not in counts:
            counts['0'] = 0
        layer_info[z] = counts

    zero_counts = list()
    for l in layer_info:
        d = layer_info[l]
        zero_counts.append((l, d['0']))

    sorted_zero_counts = sorted(zero_counts, key=lambda x: x[1])
    least_layer = sorted_zero_counts[0]

    least_0 = layer_info[least_layer[0]]
    val = least_0['1'] * least_0['2']
    print(val)


if __name__ == '__main__':
    desc = 'Advent of Code 2019'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--input', type=str, help='Input')

    args = parser.parse_args()

    main(args)
