import argparse
import numpy as np
import collections
import re
import sys


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--delimit_grammar', default='//', help='Grammar rule delineator')
    parser.add_argument('-w', '--wmap_in', help='Location to save new wmap')
    parser.add_argument('-o', '--out_idx', default='/tmp/rules.idx', help='Location to save mapped grammar')
    return parser.parse_args()

args = get_args()
rule_map = {}

with open(args.wmap_in, 'r') as f:
    for line in f:
        split = line.split()
        rule_map[' '.join(split[:-1])] = split[-1]

with open(args.out_idx, 'w') as f:
    for line in sys.stdin:
        productions = line.split(args.delimit_grammar)
        out = []
        for prod in productions:
            if prod.strip():
                out.append(rule_map[prod.strip()])
        f.write('{}\n'.format(' '.join(out)))
