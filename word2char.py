#! /usr/bin/python

import sys

lines = sys.stdin.readlines()
outdir = None
if len(sys.argv) > 1:
    outdir = sys.argv[1]

start = '<s>'
end = '</s>'
for seq_id, line in enumerate(lines):
    outname = '{}.fst.txt'.format(seq_id + 1)
    if outdir:
        outname = '{}/{}'.format(outdir, outname)
    out = ['0 1 {} {}'.format(start, start)]
    char_seq = line.split()
    for char_id, char in enumerate(char_seq):
        char_id += 1
        out.append('{} {} {} {}'.format(char_id, char_id + 1, char, char))
    out.append('{} {} {} {}'.format(len(char_seq) + 1, len(char_seq) + 2,
                                    end, end))
    out.append('{}'.format(len(char_seq) + 2))
    with open(outname, 'w') as f_out:
        f_out.write('\n'.join(out))
