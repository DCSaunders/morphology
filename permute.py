from __future__ import division
import argparse
import numpy as np

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file_in', default=None,
                        help='File of vectors to map')
    parser.add_argument('--frac', type=float, default=0.5, 
                        help='Proportion of words in sentence to permute')
    parser.add_argument('--num_swaps', type=float, default=0, 
                        help='Number of swaps to make. Overrides --frac if > 0')
    parser.add_argument('--out_file', default='/tmp/out', 
                        help='Location to save permuted sentences')
    parser.add_argument('--exclude_last', default=False, action='store_true',
                        help='Set if final token excluded from swaps')
    return parser.parse_args()



def swap(line, num_swaps, swap_count):
    swap_idx = np.random.choice(swap_count, 2 * num_swaps, replace=False)
    for i in range(num_swaps):
        line[swap_idx[2*i]], line[swap_idx[2*i + 1]] = line[swap_idx[2*i + 1]], line[swap_idx[2*i]]
    return ' '.join(line)  

def swap_n(line, num_swaps, exclude_last):
    swap_count = len(line) - 1 if exclude_last else len(line)
    if swap_count < 2 * num_swaps:
        num_swaps = swap_count // 2
        #Not enough words to swap - swapping num_swaps pairs
    return swap(split, num_swaps, swap_count)

def permute_frac(line, frac, exclude_last):
    swap_count = len(line) - 1 if exclude_last else len(line)
    num_swaps = int(frac * swap_count) // 2
    if num_swaps < 1:
        #swapping fewer than 2 words in sentence: line unchanged
        return ' '.join(line), 1
    else:
        return swap(line, num_swaps, swap_count), 0


def main(file_in, frac, num_swaps, out_file, exclude_last):
    permuted = []
    unchanged = 0
    with open(file_in, 'r') as f_in:
        for line in f_in:
            split = line.split()
            if num_swaps > 0:
                permuted.append(swap_n(split, num_swaps, exclude_last))
            else:
                s, u = permute_frac(split, frac, exclude_last)
                permuted.append(s)
                unchanged += u
    print "{} sentences unchanged".format(unchanged)
    with open(out_file, 'w') as f_out:
        for s in permuted:
            f_out.write('{}\n'.format(s))

if __name__ == '__main__':
    args = get_args()
    np.random.seed(1234)
    if args.file_in is not None:
        main(args.file_in,
             args.frac,
             args.num_swaps,
             args.out_file,
             args.exclude_last)
    else:
        print '--file_in required'
        

               
