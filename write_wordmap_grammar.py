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

ambig_terminals = set(['-RRB', '-LRB', 'N'])

def output_rule(nt, rules, ids, wmap_idx, f, f_w, most_common=None):
    for rule_rhs in rules[nt]:
        whole_rule = '{} {} {}'.format(nt, args.split_grammar, ' '.join(rule_rhs))
        if not most_common or whole_rule in most_common:
            rule_out = []
            for r in rule_rhs:
                if len(rule_rhs) == 1 and is_terminal(r, nt, rules.keys()) and r in rules.keys():
                    # some terminals are identical to non-terminals e.g. '.'
                    r = '{}-T'.format(r) 
                if r not in ids:
                    ids[r] = str(len(ids))
                rule_out.append(ids[r])
            f.write('{} : {}\n'.format(ids[nt], ' '.join(rule_out)))
            f_w.write('{} {}\n'.format(whole_rule, wmap_idx))
            wmap_idx += 1
    return wmap_idx

def is_terminal(tok, nt, nt_list):
    if tok not in nt_list:
        return True
    else:
        if tok.lower() == tok or tok in ambig_terminals:
            return True
    return False
    

delimiter = '//'
eps = '<epsilon>'
unk = 'UNK'
unk_t = '<unk>'
start = 'START'
root = 'ROOT'
eos = 'EOS'
args = get_args()
rule_counts = collections.Counter()
rules = collections.defaultdict(list) # maps nt to list of split RHSs
ids = {eps: '0', start: '1', eos: '2', unk: '3'}

if args.train_in:
    with open(args.train_in) as f:
        for line in f:
            line_rules = line.split(delimiter)
            for rule in line_rules:
                rule = rule.strip()
                if rule not in rule_counts:
                    lhs, rhs = rule.split(args.split_grammar)
                    lhs = lhs.strip()
                    rhs = rhs.strip().split()
                    rules[lhs].append(rhs)
                rule_counts.update([rule])

most_common = set()
for lhs in rules:
    terminal_est = len([rhs for rhs in rules[lhs] 
                        if len(rhs) == 1 and is_terminal(rhs[0], lhs, rules.keys())])
    if terminal_est > 1:
        unk_t_rule = '{} {} {}'.format(lhs, args.split_grammar, unk_t)
        most_common.add(unk_t_rule)
        rules[lhs].append([unk_t])

if args.vocab_size:
    for rule, _ in rule_counts.most_common(args.vocab_size - len(most_common)):
        most_common.add(rule)


for idx, nt in enumerate(rules, start=len(ids)):
    ids[nt] = str(idx)
rules[eps].append([eps]) # epsilon rule
rules[start].append([root, eos]) # start rule
rules[eos].append([eps]) # eos rule
rules[unk].append([unk]) # unk rule

with open(args.grammar_out, 'w') as f, open(args.wmap_out, 'w') as f_w:
    output_rule(eps, rules, ids, 0, f, f_w)
    output_rule(start, rules, ids, 1, f, f_w)
    output_rule(eos, rules, ids, 2, f, f_w)
    output_rule(unk, rules, ids, 3, f, f_w)
    wmap_idx = 4
    rules.pop(eps)
    rules.pop(start)
    rules.pop(eos)
    rules.pop(unk)
    for nt in rules:
        wmap_idx = output_rule(nt, rules, ids, wmap_idx, f, f_w, most_common)
