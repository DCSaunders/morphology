import argparse
import numpy as np
import collections
import sys

def is_terminal(tok, nt):
    if tok.lower() == tok and nt.lower() == nt:
        # "ADJP ==> ''" is a non-terminal, ", ==> ," is a terminal
        return True
    elif tok.upper() != tok:
        return True
    return False


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--delimit_grammar', default='//', help='Grammar rule delimiter')
    parser.add_argument('-u', '--unk', default='<unk>')
    parser.add_argument('--unk_id', type=int, default=3)
    parser.add_argument('-r', '--root', default='ROOT')
    parser.add_argument('-w', '--wmap_in', default='wmap', help='Location to load wmap')
    parser.add_argument('-o', '--out_idx', default='idx', help='Location to save mapped out')
    parser.add_argument('-i2g', '--to_grammar', default=False, 
                        action='store_true', help='True if idx->rules')
    parser.add_argument('-i2w', '--to_word', default=False, 
                        action='store_true', help='True if idx->words')
    return parser.parse_args()

args = get_args()
wmap = {}
reverse = args.to_word or args.to_grammar
cutoff_idx = 5
with open(args.wmap_in, 'r') as f_in:
    for line in f_in:
        tok, idx = line.split()
        if tok.upper() != tok and cutoff_idx == 5 and int(idx) > cutoff_idx:
            cutoff_idx = int(idx)
        if tok in wmap:
            tok = '{}_T'.format(tok)
            if cutoff_idx == 5 and int(idx) > cutoff_idx:
                cutoff_idx = int(idx)
        wmap[tok] = idx
        
if reverse:
    wmap = {v: k for k, v in wmap.items()}
    for idx, tok in wmap.items():
        if tok.upper() == tok and len(tok) >= 3 and tok[-2:] == '_T':
            wmap[idx] = tok[:-2]
    with open(args.out_idx, 'w') as f:
        for line in sys.stdin:
            line = line.strip()
            if args.to_grammar:
                out = [wmap[prod] for prod in line.split()]
            else:
                out = [wmap[prod] for prod in line.split()
                       if int(prod) >= cutoff_idx or int(prod) == args.unk_id]
            f.write('{}\n'.format(' '.join(out)))
else:        
    delimiter = '//'
    joiner = ' ==> '
    with open(args.out_idx, 'w') as f:
        for line in sys.stdin:
            line = line.strip()
            productions = line.split(delimiter)
            out = [wmap[args.root]]
            for prod in productions:
                if prod:
                    out.append(wmap[delimiter])
                    prod = prod.strip()
                    lhs, rhs = prod.split(joiner)
                    rhs = rhs.split()
                    if len(rhs) == 1 and is_terminal(rhs[0], lhs) and rhs[0].upper() == rhs[0]:
                        rhs[0] = '{}_T'.format(rhs[0])
                    for tok in rhs:
                        if tok in wmap:
                            out.append(wmap[tok])
                        else:
                            out.append(wmap[args.unk])
            f.write('{}\n'.format(' '.join(out)))

