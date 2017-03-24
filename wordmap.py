import argparse
import collections
import string

UNK = 'UNK'
NUM = '<NUM>'
PUNC = string.punctuation

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_in', help='File of vectors to map')
    parser.add_argument('--vocab_size', type=int, default=0, 
                        help='Vocab size to use constructing word map')
    parser.add_argument('--lowercase', default=False, action='store_true',
                        help='True if lowercasing')
    parser.add_argument('--punc', default=True, action='store_false',
                        help='True if keeping punctuation, otherwise stripped')
    parser.add_argument('--wmap', help='Location of wordmap to apply')
    parser.add_argument('--out_dir', default='/tmp', 
                        help='Location to save idx/wmap')
    parser.add_argument('--file_out', default='/tmp/out.en', 
                        help='Location to save reverse wordmapped data')
    parser.add_argument('--reverse', default=False, action='store_true', 
                        help='True if reversing wordmap (id to word)')
    parser.add_argument('--norm_digits', default=False, action='store_true', 
                        help='True if replacing any digits with <NUM> token')
    return parser.parse_args()

def construct_wmap(f_in, wmap, vocab_size, lowercase, keep_punc, norm_digits):
    # Construct a wordmap from the text file with a given vocab size and 
    # optional lowercasing.
    c = collections.Counter()
    with open(f_in, 'r') as f:
        for line in f:
            if lowercase:
                line = line.lower()
            c.update(line.split())
    if not keep_punc:
        strip_punc(c)
    if norm_digits:
        normalise_digits(c)
    if vocab_size == 0:
        vocab_size = len(c) + 3
    index = len(wmap)
    for pair in c.most_common(vocab_size - 3):
        wmap[pair[0]] = index
        index += 1

def strip_punc(counter):
    # Remove any punctuation from the wordmap counter
    for punc in PUNC:
        del counter[punc]

def normalise_digits(counter):
    for k in counter.keys():
        if has_num(k):
            del counter[k]

def has_num(token):
    for l in token:
        if l.isdigit():
            return True
    return False

def save_wmap(out_dir, wmap):
    # Save wmap
    with open (out_dir + '/wmap', 'w') as f:
        for key in sorted(wmap, key=lambda x: wmap[x]):
            f.write('{} {}\n'.format(key, wmap[key]))

def read_wmap(f_in, wmap):
    # Read wmap file line-by-line and pass to dictionary
    with open(f_in, 'r') as f:
        for line in f:
            tok, index = line.split()
            wmap[tok] = index

def apply_wmap(src, wmap, out_dir, lowercase, keep_punc, norm_digits):
    # Apply wmap to input file line-by-line and save output
    with open(src, 'r') as f_in, open('{}/out.idx'.format(out_dir), 'w') as f_out:
        for line in f_in:
            if lowercase:
                line = line.lower()
            out = []
            for tok in line.split():
                if tok in wmap:
                    out.append(str(wmap[tok]))
                elif norm_digits and has_num(tok):
                    out.append(str(wmap[NUM]))
                elif not keep_punc and tok in PUNC:
                    continue
                else:
                    out.append(str(wmap[UNK]))
            f_out.write(' '.join(out) + '\n')
            #print(' '.join(out) + '\n')
    
def reverse_wmap(file_in, out_file, wmap):
    reverse_wmap = {idx: word for word, idx in wmap.items()}
    with open(file_in, 'r') as f_in, open(out_file, 'w') as f_out:
        for line in f_in:
            out = []
            for idx in line.split():
                if not idx.isdigit():
                    f_out.write(line)
                    break
                else:
                    out.append(reverse_wmap[idx.strip()])
            f_out.write(' '.join([str(tok) for tok in out]) + '\n')

if __name__ == '__main__':
    args = get_args()
    if args.lowercase:
        UNK = 'unk'
    wmap = {'<epsilon>': 0, '<s>': 1, '</s>': 2, UNK: 3, NUM: 4}
    if args.wmap:
        read_wmap(args.wmap, wmap)
    if args.reverse:
        reverse_wmap(args.file_in, args.file_out, wmap)
    else:
        if not args.wmap:
            construct_wmap(args.file_in, wmap, args.vocab_size, args.lowercase, args.punc, args.norm_digits)
            save_wmap(args.out_dir, wmap)
        apply_wmap(args.file_in, wmap, args.out_dir, args.lowercase, args.punc, args.norm_digits)
               
