import argparse
import numpy as np
import collections
import re
import sys
# take list of rules through STDIN, output wordmap and non-terminal grammar

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--vocab_size', type=int, default=0, help='Vocab size for wmap, 0 if whole vocab.')
    parser.add_argument('-s', '--split_grammar', default='==>', help='Grammar rule delineator')
    parser.add_argument('-w', '--wmap_out', default='/tmp/wmap', help='Location to save new wmap')
    parser.add_argument('-o', '--grammar_out', default='/tmp/grammar', help='Location to save mapped grammar')
    parser.add_argument('-t', '--train_in', default=None, help='Location of training data')
    return parser.parse_args()

def output_rule(nt, rules, ids, wmap_idx, f, f_w, most_common=None):
    for rule_rhs in rules[nt]:
        whole_rule = '{} {} {}'.format(nt, args.split_grammar, ' '.join(rule_rhs))
        if not most_common or whole_rule in most_common:
            rule_out = []
            for r in rule_rhs:
                if len(rule_rhs) == 1 and r == nt and r not in (eps, unk):
                    # some terminals are identical to non-terminals e.g. '.'
                    r = '{}-T'.format(r) 
                if r not in ids:
                    ids[r] = str(len(ids))
                rule_out.append(ids[r])
            f.write('{} : {}\n'.format(ids[nt], ' '.join(rule_out)))
            f_w.write('{} {}\n'.format(whole_rule, wmap_idx))
            wmap_idx += 1
    return wmap_idx

delimiter = '//'
eps = '<epsilon>'
unk = 'UNK'
start = 'START'
root = 'ROOT'
args = get_args()
rule_counts = collections.Counter()
rules = collections.defaultdict(list) # maps nt to list of split RHSs
ids = {eps: '0', start: '1', unk: '2'}

if args.train_in:
    with open(args.train_in) as f:
        for line in f:
            line_rules = line.split(delimiter)
            rule_counts.update([rule.strip() for rule in line_rules 
                                if rule.strip()])

most_common = set()
if args.vocab_size:
    for rule, _ in rule_counts.most_common(args.vocab_size):
        most_common.add(rule)
        lhs, rhs = rule.split(args.split_grammar)
        rules[lhs.strip()].append(rhs.split())

for idx, nt in enumerate(rules, start=3):
    ids[nt] = str(idx)
rules[eps].append([eps])
rules[unk].append([unk])
rules[start].append([root])
with open(args.grammar_out, 'w') as f, open(args.wmap_out, 'w') as f_w:
    output_rule(eps, rules, ids, 0, f, f_w)
    output_rule(start, rules, ids, 1, f, f_w)
    output_rule(unk, rules, ids, 2, f, f_w)
    wmap_idx = 3
    rules.pop(eps)
    rules.pop(unk)
    rules.pop(start)
    for nt in rules:
        wmap_idx = output_rule(nt, rules, ids, wmap_idx, f, f_w, most_common)
