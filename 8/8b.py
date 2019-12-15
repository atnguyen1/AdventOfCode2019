#!/usr/bin/env python

from __future__ import print_function

import argparse
import sys

from collections import Counter


def grab_layers(input, width):
    for i in xrange(0, len(input), width):
        yield input[i:i + width]


def main(args):
    data = list()
    with open(args.input, 'r') as fh:
        for line in fh:
            line = line.rstrip()
            data += line

    img_height = 6
    img_width = 25

    layers = grab_layers(data, img_height * img_width)

    # Format into correct matrix of img_width by img_height
    all_layers = list()
    for l in layers:
        layer_data = list()
        for r in grab_layers(l, img_width):
            layer_data.append(r)
        all_layers.append(layer_data)

    # reformat into image stacks, simply a transpose operation

    y_stack = list()
    for y in range(0, img_height):
        x_stack = list()
        for x in range(0, img_width):
            z_stack = list()
            for z in range(0, len(all_layers)):
                z_stack.append(all_layers[z][y][x])
            x_stack.append(z_stack)
        y_stack.append(x_stack)

    final_image = list()

    # Find first colored pixel, black = 0, white = 1, transparent = 2
    final_y = list()

    for y in range(0, len(y_stack)):
        final_x = list()
        for x in range(0, len(x_stack)):
            pixel_data = y_stack[y][x]
            smallest_1 = None
            smallest_0 = None

            # Find first 1 or 0
            for layer, p in enumerate(pixel_data):
                if p == '0':
                    if smallest_0 is None:
                        smallest_0 = layer
                        continue
                elif p == '1':
                    if smallest_1 is None:
                        smallest_1 = layer
                        continue
            if smallest_1 is None:
                pixel = 0
            elif smallest_0 is None:
                pixel = 1
            else:
                if smallest_1 < smallest_0:
                    pixel = 1
                else:
                    pixel = 0

            # print(pixel_data)
            # print(pixel)
            final_x.append(pixel)
        # print(''.join([str(x) for x in final_x]))
        final_y.append(final_x)

    for y in range(0, len(final_y)):
        print(''.join([str(x) if x == 1 else ' ' for x in final_y[y]]))


    '''
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
    '''

if __name__ == '__main__':
    desc = 'Advent of Code 2019'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--input', type=str, help='Input')

    args = parser.parse_args()

    main(args)
