import argparse
import numpy as np
import collections
import re
import sys


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--vocab_size', type=int, default=0, help='Vocab size for wmap, 0 if whole vocab')
    parser.add_argument('-l', '--lowercase', default=False, action='store_true', help='True if lowercasing')
    parser.add_argument('-s', '--split_grammar', default='==>', help='Grammar rule delineator')
    parser.add_argument('-w', '--wmap_out', default='/tmp/wmap', help='Location to save new wmap')
    parser.add_argument('-o', '--grammar_out', default='/tmp/wmap', help='Location to save mapped grammar')
    return parser.parse_args()

def prods_to_eq(prods):
    seq = [prods[0].lhs()]
    for prod in prods:
        if str(prod.lhs()) == 'Nothing':
            break
        for ix, s in enumerate(seq):
            if s == prod.lhs():
                seq = seq[:ix] + list(prod.rhs()) + seq[ix+1:]
                break
    try:
        return ''.join(seq)
    except:
        return ''

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

with open(args.grammar_out, 'w') as f:
    for nt in rules:
        for rule in rules[nt]:
            rule_out = []
            for r in rule:
                if r not in ids:
                    if args.lowercase:
                        r = r.lower()
                    ids[r] = str(len(ids))
                rule_out.append(ids[r])
            f.write('{} : {}\n'.format(ids[nt], ' '.join(rule_out)))

reverse = {v: k for k, v in ids.items()}
with open(args.wmap_out, 'w') as f:
    for i in range(len(ids)):
        idx = str(i)
        f.write('{} {}\n'.format(reverse[idx], idx))
