#! /usr/bin/python

import sys

lines = sys.stdin.readlines()
outdir = None
ivchars = set()
if len(sys.argv) >= 2:
    outdir = sys.argv[1]
    ivsyms = sys.argv[2]
    with open(ivsyms, 'r') as f_in:
        for line in f_in:
            ivchars.add(line.split()[0])
        
unk = '<unk>'
start = '<s>'
end = '</s>'
eps_found = False
for seq_id, line in enumerate(lines):
    seq_id += 1
    outname = '{}.fst'.format(seq_id)
    if outdir:
        outname = '{}/{}'.format(outdir, outname)
    out = ['0 1 {} {}'.format(start, start)]
    char_seq = line.split()
    for char_id, char in enumerate(char_seq):
        char_id += 1
        if char not in ivchars:
            char = unk
        out.append('{} {} {} {}'.format(char_id, char_id + 1, char, char))
    out.append('{} {} {} {}'.format(len(char_seq) + 1, len(char_seq) + 2,
                                    end, end))
    out.append('{}'.format(len(char_seq) + 2))
    with open(outname, 'w') as f_out:
        f_out.write('\n'.join(out))
