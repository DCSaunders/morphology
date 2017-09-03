import argparse
import collections
import copy
import sys

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--vocab_size', type=int, default=0, help='Terminal vocab size for wmap, 0 if whole vocab.')
    parser.add_argument('-s', '--split_grammar', default='==>', help='Grammar rule delineator')
    parser.add_argument('-w', '--wmap_out', default='wmap', help='Location to save new wmap')
    parser.add_argument('-o', '--grammar_out', default='ntmap', help='Location to save mapped grammar')
    parser.add_argument('-t', '--train_in', default=None, help='Location of training data')
    return parser.parse_args()

def is_terminal(tok, nt):
    if tok.lower() == tok and nt.lower() == nt:
        # "ADJP ==> ''" is a non-terminal, ", ==> ," is a terminal
        return True
    elif tok.upper() != tok:
        return True
    return False

def update_ids(to_add, ids):
    start_idx = len(ids)
    for idx, tok in enumerate(to_add):
        ids[tok] = start_idx + idx

delimiter = '//'
eps = '<epsilon>'
unk = '<unk>'
start = 'START'
root = 'ROOT'
eos = 'EOS'
eor = '</R>' # marker for last NT in rule
args = get_args()
ids = {eps: 0, start: 1, eos: 2, unk: 3}
terminals = collections.Counter()
can_follow = collections.defaultdict(set)
terminal_nts = set()

if not args.train_in:
    sys.exit()
with open(args.train_in, 'r') as f_in:
    for line in f_in:
        line = line.strip('\n')
        rules = [r.strip() for r in line.split(delimiter) if r.strip()]
        for rule in rules:
            lhs, rhs = rule.split(' ==> ')
            rhs = rhs.split()
            if len(rhs) == 1 and is_terminal(rhs[0], lhs):
                if rhs[0].upper() == rhs[0]:
                    rhs[0] = '{}_T'.format(rhs[0])
                terminal_nts.add(lhs)
                terminals.update(rhs)
                can_follow[lhs].add(rhs[0])
            else:
                for tok in rhs:
                    can_follow[lhs].add(tok)
                    can_follow[lhs].add('{}{}'.format(tok, eor))

if args.vocab_size:
    vocab_terminals = set([item[0] for item in terminals.most_common(args.vocab_size)])
else:
    vocab_terminals = set(terminals.keys())

for nt in terminal_nts:
    can_follow[nt].add(unk)

nts = can_follow.keys()
update_ids(nts, ids)
last_nts = []
for nt in nts:
    new_nt = '{}{}'.format(nt, eor)
    last_nts.append(new_nt)
    can_follow[new_nt] = copy.deepcopy(can_follow[nt])
    can_follow[new_nt].add(eps)
update_ids(last_nts, ids)
update_ids(vocab_terminals, ids)
can_follow[start].add(root)
can_follow[eos].add(eos)


with open(args.wmap_out, 'w') as f_out:
    for tok in sorted(ids, key=lambda x: ids[x]):
        idx = ids[tok]
        if tok.upper() == tok and len(tok) >= 3 and tok[-2:] == '_T':
            tok = tok[:-2]
        f_out.write('{} {}\n'.format(tok, idx))
        
with open(args.grammar_out, 'w') as f_out:
    for nt in can_follow.keys():
        follow_ids = [str(ids[tok]) for tok in can_follow[nt] if tok in ids]
        f_out.write('{} : {}\n'.format(ids[nt], ' '.join(follow_ids)))
