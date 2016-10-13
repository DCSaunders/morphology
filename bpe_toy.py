#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Toy example of Byte Pair Encoding approach to morphological decomposition given in Neural Machine Translation of rare words with subword units
(Sennrich et al, 2015, https://arxiv.org/abs/1508.07909)
'''
import collections
import re

def get_stats(vocab):
    pairs = collections.defaultdict(int)
    for word, freq in vocab.items():
        symbols = word.split()
        for i in range(len(symbols) - 1):
            pairs[symbols[i], symbols[i + 1]] += freq
    return pairs


def merge_vocab(pair, vocab_in):
    vocab_out = {}
    bigram = re.escape(' '.join(pair))
    joined_pair = re.compile(r'(?<!\S)' + bigram + r'(?!\S)')
    for word in vocab_in:
        word_out = joined_pair.sub(''.join(pair), word)
        vocab_out[word_out] = vocab_in[word]
    return vocab_out


if __name__ == '__main__': 
    vocab = {'h a r d e r </w>': 1, 'b e t t e r </w>': 1,
             'f a s t e r </w>': 1, 's t r o n g e r </w>': 1}
    num_merges = 4
    for i in range(num_merges):
        pairs = get_stats(vocab)
        best = max(pairs, key=lambda x: pairs[x])
        vocab = merge_vocab(best, vocab)
    print vocab
