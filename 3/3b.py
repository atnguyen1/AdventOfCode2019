#!/usr/bin/env python

from __future__ import print_function

import argparse
import math
import sys


def main(args):
    data = []
    with open(args.input, 'r') as fh:
        for line in fh:
            line = line.rstrip().split(',')
            data.append(line)

    # Test
    # data = [['R8', 'U5', 'L5', 'D3'], ['U7', 'R6', 'D4', 'L4']]   # 15
    # data = [['R75','D30','R83','U83','L12','D49','R71','U7','L72'],  
    #         ['U62','R66','U55','R34','D71','R55','D58','R83']]   # 610
    # data = [['R98','U47','R26','D63','R33','U87','L62','D20','R33','U53','R51'],
    #         ['U98','R91','D20','R16','D67','R40','U7','R15','U6','R7']]   # 410

    wire_points = list()
    for wire in data:
        points = [(0, 0)]
        posx = 0
        posy = 0
        for direction in wire:
            d = direction[0]
            l = int(direction[1:])
            if d == 'R':
                posx += l
            if d == 'L':
                posx -= l
            if d == 'U':
                posy += l
            if d == 'D':
                posy -= l
            points.append((posx, posy))
        wire_points.append(points)

    # Determine intersection by overlap
    w1 = wire_points[0]
    w2 = wire_points[1]
    # print(wire_points)

    # Turn points into line segments which are point pairs
    wire_segment1 = list()
    wire_segment2 = list()

    for xi in range(0, len(w1[:-1])):
        line1 = (w1[xi], w1[xi + 1])
        wire_segment1.append(line1)

    for yi in range(0, len(w2[:-1])):
        line2 = (w2[yi], w2[yi + 1])
        wire_segment2.append(line2)

    # print(wire_segment1)
    # print(wire_segment2)

    # compare lines and record intersection points
    # lines intersect if they are vertical + horizontal
    # if double vertical or double horizontal continue
    # x == y means that they intersect, check bounds
    # then iterate to get to the intersection point
    intersection = list()
    steps_2_intersection = list()
    steps_wire1 = 0
    steps_wire2 = 0

    ordered_interactions = list()

    #             steps_wire1 += abs(p1[0] - p2[0])
    #             steps_wire2 += abs(p3[0] - p4[0])
    orientation1 = dict()
    orientation2 = dict()
    for xi, entry in enumerate(wire_segment1):
        l1horz = None
        l1vert = None
        p1 = entry[0]
        p2 = entry[1]
        if p2[1] - p1[1] == 0:
            l1horz = True
            l1vert = False
        else:
            l1horz = False
            l1vert = True
        orientation1[xi] = l1horz
        # print(l1horz)
        # print(l1vert)

        for yi, entry2 in enumerate(wire_segment2):
            l2horz = None
            l2vert = None
            p3 = entry2[0]
            p4 = entry2[1]
            # Determine horizontal or vert line
            if p3[1] - p4[1] == 0:
                # Horizontal line
                l2horz = True
                l2vert = False
            else:
                l2horz = False
                l2vert = True
            orientation2[yi] = l2horz
            # print(l2horz)
            # print(l2vert)

            if l2horz == l1horz:
                # Count steps
                continue

            elif l2vert == l1vert:
                continue

            # print(entry, entry2)
            # print(l1horz, l1vert, l2horz, l2vert)

            # P1       P2       P3      P4
            # ((8, 5), (3, 5)) ((6, 7), (6, 3))
            # True False False True
            # Check bounds
            if l1horz and l2vert:
                tp1 = p1
                tp2 = p2
                tp3 = p3
                tp4 = p4

                if tp1[0] > tp2[0]:
                    temp = tp1
                    tp1 = tp2
                    tp2 = temp
                if tp3[1] < tp4[1]:
                    temp2 = tp3
                    tp3 = tp4
                    tp4 = temp2

            elif l2horz and l1vert:
                tp1 = p3
                tp2 = p4
                tp3 = p1
                tp4 = p2

                if tp1[0] > tp2[0]:
                    temp = tp1
                    tp1 = tp2
                    tp2 = temp
                if tp3[1] < tp4[1]:
                    temp2 = tp3
                    tp3 = tp4
                    tp4 = temp2

            # print(tp1, tp2, tp3, tp4)

            if (tp3[0] > tp1[0]) and (tp3[0] < tp2[0]):
                if (tp1[1] > tp4[1]) and (tp1[1] < tp3[1]):
                    intersection.append((tp3[0], tp1[1]))
                    ordered_interactions.append((xi, yi, l1horz, l2horz))

    # print("Intersections")
    # print(intersection)
    dist = list()
    for i in intersection:
        distance = abs(0 - i[0]) + abs(0 - i[1])
        dist.append(distance)

    # print("Ordered Lines with intersections")
    # print(ordered_interactions)

    all_data = dict()

    for intersect, o in zip(intersection, ordered_interactions):
        wire1_cross = o[0]
        wire2_cross = o[1]
        l1horz = o[2]
        l2horz = o[3]

        wire1_steps = 0
        wire2_steps = 0

        # print(intersect)
        # print(o)
        for i, ws1 in enumerate(wire_segment1):
            if wire1_cross == i:
                if l1horz:
                    df1 = abs(ws1[0][0] - intersect[0])
                    wire1_steps += df1
                    # print(df1)
                    break
                else:
                    # Vert
                    df1 = abs(ws1[0][1] - intersect[1])
                    wire1_steps += df1
                    # print(df1)
                    break
            else:
                p1 = ws1[0]
                p2 = ws1[1]
                if orientation1[i]:
                    d1 = abs(p1[0] - p2[0])
                else:
                    d1 = abs(p1[1] - p2[1])
                wire1_steps += d1
                # print(d1)
        # print('ws1')
        # print(wire1_steps)

        for j, ws2 in enumerate(wire_segment2):
            if wire2_cross == j:
                if l2horz:
                    df2 = abs(ws2[0][0] - intersect[0])
                    wire2_steps += df2
                    # print(df2)
                    break
                else:
                    # Vert
                    df2 = abs(ws2[0][1] - intersect[1])
                    wire2_steps += df2
                    # print(df2)
                    break
            else:
                p3 = ws2[0]
                p4 = ws2[1]
                if orientation2[j]:
                    d2 = abs(p3[0] - p4[0])
                else:
                    d2 = abs(p3[1] - p4[1])
                wire2_steps += d2
        # print('ws2')
        # print(wire2_steps)

        all_data[intersect] = (wire1_steps, wire2_steps, wire1_steps + wire2_steps)

    # print(all_data)

    sorted_distance = dict()
    for key in all_data:
        distances = all_data[key]
        sumdist = distances[2]
        sorted_distance[sumdist] = key

    # print(sorted(sorted_distance.keys()))
    short = sorted(sorted_distance.keys())[0]

    print('Minimum Steps')
    print(short)
    print('Short route to intersection at')
    print(sorted_distance[short])
    print('Manhatten Distance')
    print(sorted_distance[short][0] + sorted_distance[short][1])


if __name__ == '__main__':
    desc = 'Advent of Code 2019'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--input', type=str, help='Mass')

    args = parser.parse_args()

    main(args)
