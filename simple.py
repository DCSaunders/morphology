import string

PUNC = set([p for p in string.punctuation])

def space_punctuation(word):
    out = []
    s = ''
    idx = 0
    while idx < len(word):
        last = (idx == len(word) - 1)
        l = word[idx]
        if l in PUNC:
            if s and l != '-':
                out.append(s)
                s = ''
            if l == "'":
                idx = adjust_apostrophe(out, word, idx, last)
            elif not last:
                if ((idx < len(word) - 2)
                    and l == '.'
                    and l == word[idx + 1]
                    and l == word[idx + 2]):
                    out.append('...')
                    idx += 3
                elif (l == '-' and l == word[idx + 1]):
                    out.append(s)
                    s = ''
                    out.append('--')
                    idx += 2
                elif l == '-':
                    s += '-'
                    idx += 1
                else:
                    out.append(l)
                    idx += 1
            else:
                out.append(l)
                idx += 1
        else:
            s += l
            idx += 1
    out.append(''.join(s))
    return out
            
def adjust_apostrophe(out, word, idx, last):
    last_seg = out[-1]
    if last:
        if last_seg[-1] == 's':
            out.append("'s")
        else:
            out.append("'")
        return idx + 1
    elif last_seg[-1] == 'n' and word[idx + 1] == 't':
        out[-1] = last_seg[:-1]
        out.append("n't")
        return idx + 2
    else:
        new_seg = ["'"]
        idx += 1
        while idx < len(word):
            if word[idx] not in PUNC:
                new_seg.append(word[idx])
                idx += 1
            else:
                break
        out.append(''.join(new_seg))
        return idx

