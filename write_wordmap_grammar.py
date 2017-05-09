import argparse
import numpy as np
import collections
import re
import sys


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--vocab_size', type=int, default=0, help='Vocab size for wmap, 0 if whole vocab')
    parser.add_argument('-s', '--split_grammar', default='==>', help='Grammar rule delineator')
    parser.add_argument('-w', '--wmap_out', default='/tmp/wmap', help='Location to save new wmap')
    parser.add_argument('-o', '--grammar_out', default='/tmp/grammar', help='Location to save mapped grammar')
    return parser.parse_args()

eps = '<epsilon>'
args = get_args()
rules = collections.defaultdict(list)
ids = {eps: '0'}
for line in sys.stdin:
    lhs, rhs = line.strip('\n').split(args.split_grammar)
    rules[lhs.strip()].append(rhs.split())

for idx, nt in enumerate(rules, start=1):
    ids[nt] = str(idx)
rules[eps].append([eps])

wmap_idx = 0
with open(args.grammar_out, 'w') as f, open(args.wmap_out, 'w') as f_w:
    for nt in rules:
        for rule in rules[nt]:
            rule_out = []
            for r in rule:
                if r not in ids:
                    ids[r] = str(len(ids))
                rule_out.append(ids[r])
            f.write('{} : {}\n'.format(ids[nt], ' '.join(rule_out)))
            f_w.write('{} {} {} {}\n'.format(
                nt, args.split_grammar, ' '.join(rule), wmap_idx))
            wmap_idx += 1
