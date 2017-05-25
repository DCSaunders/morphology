import argparse
import collections
import sys

parser = argparse.ArgumentParser()
parser.add_argument('-t', '--train', help='training rules')
parser.add_argument('-s', '--strip', default=False, action='store_true',
                    help='strip semantic/grammatical function annotations')
parser.add_argument('-c', '--count', default=False, action='store_true',
                    help='output counts')
parser.add_argument('-o', '--output', default=False, action='store_true',
                    help='output stripped data')
parser.add_argument('-r', '--rules', default=False, action='store_true',
                    help='output stripped rule list')

args = parser.parse_args()

train_set = set()
test_set = set()
unseen_terminal = set()
delimiter = '//'
# phase II semantic/grammatical function annotation list from 
# http://www.surdeanu.info/mihai/teaching/ista555-fall13/readings/PennTreebankConstituents.html
annotations = set(['VOC', 'DIR', 'LOC', 'MNR', 'PRP', 'TMP', 'BNF', 'EXT', 'SBJ', 'LGS', 'ADV', 'DTV', 'NOM', 'PRD', 'CLF', 'TPC', 'PUT', 'CLR', 'CLF', 'HLN', 'TTL'])

def strip_annotations(rule):
    out = []
    for sym in rule.split():
        split_sym = sym.split('-')
        if len(split_sym) > 1 and split_sym[0] and sym.lower() != sym:
            strip_sym = []
            for s in split_sym:
                if s not in annotations:
                    strip_sym.append(s)
            out.append('-'.join(strip_sym))
        else:
            # keep terminals, symbols like -LRB and --, and untagged symbols
            out.append(sym)
    return ' '.join(out)

with open(args.train, 'r') as f:
    for line in f:
        seq = line.split(delimiter)
        for rule in seq:
            rule = rule.strip()
            if args.strip:
                rule = strip_annotations(rule)
            if rule:
                train_set.add(rule)
            
if args.output or args.count:
    rule_count = collections.Counter()
    for line in sys.stdin:
        seq = line.split(delimiter)
        out_seq = []
        for rule in seq:
            rule = rule.strip()
            if args.strip:
                rule = strip_annotations(rule)
                out_seq.append(rule)
            test_set.add(rule)
            rule_count.update([rule])
        if args.strip and args.output:
            print ' {} '.format(delimiter).join(out_seq)


unseen = test_set - train_set
for rule in unseen:
    rhs = ' '.join(rule.split()[2:])
    if rhs.lower() == rhs:
        # rhs is terminal only
        unseen_terminal.add(rule)

unseen_nonterminal = unseen - unseen_terminal
if args.count:
    print len(train_set)
    print len(test_set)
    print len(unseen)
    print len(unseen_nonterminal)
    common_count = 0
    for rule, count in rule_count.most_common():
        if count == 1:
            common_count += 1
            print rule, count
    print common_count

if args.rules:
    for rule in train_set:
        print rule
