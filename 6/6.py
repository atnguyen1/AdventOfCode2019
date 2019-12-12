#!/usr/bin/env python

from __future__ import print_function

import argparse
import sys


# class Tree

orbit_map = dict()


class Tree:
    def __init__(self, node):
        self.node = node
        self.children = []
        self.distance_to_com = None

    def get_label(self):
        return(self.node)

    def get_children(self):
        return self.children

    def add_child_by_id(self, child):
        if not self.is_child(child):
            new_child = Tree(child)
            self.children.append(new_child)
        else:
            print('Attempting to add existing child', child)

    def get_child(self, child):
        for c in self.children:
            if c.get_label() == child:
                return c
        return None

    def print_children(self):
        for c in self.children:
            print(c.get_label())

    def is_child(self, child):
        for c in self.children:
            if c.get_label == child:
                return True

        return False

    def show_full(self):
        print(self, '-', self.distance_to_com)
        for c in self.children:
            c.show_full()

    def set_distance_2_com(self, dist):
        self.distance_to_com = dist

    def get_distance_2_com(self):
        return self.distance_to_com

    def __repr__(self):
        out_str = self.node + ')'
        for c in self.children:
            out_str += c.get_label() + ','
        return out_str


# Recursion
# Mutator
def build_tree(tree, children_to_add):
    processing = list()

    if children_to_add == []:
        return []

    for ch in children_to_add:
        tree.add_child_by_id(ch)
        processing.append(ch)

    # Continue building tree from children
    for p in processing:
        sub_tree = tree.get_child(p)

        if sub_tree:
            build_tree(sub_tree, orbit_map[sub_tree.get_label()])
        else:
            print('Failure to fetch child', p)


def set_distances(tree, depth, leaf):
    # Checksum Calculations
    # follow and set all leaves
    if tree.get_label() == leaf:
        tree.set_distance_2_com(depth)
        return
    else:
        tree.set_distance_2_com(depth)
        depth += 1
        for c in tree.get_children():
            set_distances(c, depth, leaf)


def get_distances(tree, node):
    if tree.get_label() == node:
        return tree.get_distance_2_com()
    else:
        for c in tree.get_children():
            res = get_distances(c, node)
            if res:
                return res


def main(args):
    global orbit_map
    nodes = list()
    leafs = list()

    all_nodes = list()

    data = list()
    with open(args.input, 'r') as fh:
        for line in fh:
            line = line.rstrip().split(',')
            data += line

    # Place orbits in key:val store
    for d in data:
        orbits = d.split(')')
        alpha = orbits[0]
        beta = orbits[1]

        # Alpha is the object that beta orbits around.
        if alpha in orbit_map:
            orbit_map[alpha].append(beta)
        else:
            orbit_map[alpha] = [beta]
        nodes.append(alpha)
        nodes.append(beta)
        all_nodes.append(alpha)
        all_nodes.append(beta)

    # Clean up and add leafs as they have null as orbit values
    orbital_bodies = set(orbit_map.keys())
    leafs = set(nodes).difference(orbital_bodies)

    for l in leafs:
        orbit_map[l] = []
        all_nodes.append(l)

    all_nodes = list(set(all_nodes))
    # print(orbit_map)

    # Build tree
    init = Tree('COM')
    build_tree(init, orbit_map['COM'])
    # init.show_full()
    for l in leafs:
        set_distances(init, 0, l)
    # print('BREAK')
    # init.show_full()
    # print(get_distances(init, 'COM'))

    sum_dist = 0
    for n in all_nodes:
        n_dist = get_distances(init, n)
        sum_dist += n_dist
        # print(n, n_dist)
    print('Checksum', sum_dist)


if __name__ == '__main__':
    desc = 'Advent of Code 2019 Part 6'
    parser = argparse.ArgumentParser(description=desc)
    parser.add_argument('--input', type=str, help='Mass')

    args = parser.parse_args()

    main(args)
