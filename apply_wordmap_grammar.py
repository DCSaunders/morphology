import argparse
import numpy as np
import collections
import sys


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--delimit_grammar', default='//', 
                        help='Grammar rule delimiter')
    parser.add_argument('-w', '--wmap_in', help='Location to load wmap')
    parser.add_argument('-o', '--out_idx', default='/tmp/idx', help='Location to save mapped out')
    parser.add_argument('-i2g', '--to_grammar', default=False, 
                        action='store_true', help='True if idx->rules')
    parser.add_argument('-i2w', '--to_words', default=False, 
                        action='store_true', help='True if idx->words')

    return parser.parse_args()

args = get_args()
rule_map = {}

with open(args.wmap_in, 'r') as f:
    for line in f:
        split = line.split()
        rule_map[' '.join(split[:-1])] = split[-1]

if args.to_words or args.to_grammar:
    # TODO
    # If mapping to words, need to map to grammar rules first, reverse wmap,
    # and have set of non-terminals to cut out after reversing
    # space-join if idx or word out. delimiter-join if grammar out.
    joiner = ' {} '.format(args.delimit_grammar)
else:
    joiner = ' '


with open(args.out_idx, 'w') as f:
    for line in sys.stdin:
        productions = line.split(args.delimit_grammar)
        out = []
        for prod in productions:
            if prod.strip():
                out.append(rule_map[prod.strip()])
        f.write('{}\n'.format(joiner.join(out)))
