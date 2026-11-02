"""Load the transcription, key and reading from data/."""
import os
import re

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data')


def load(fn='tr1.txt'):
    """Return (page, kind, value): kind 'c' is a number word (list of signs), 'p' a run of plain text.
    A trailing comma carries a word to the next line. ~NN is a number the writer struck out with dots."""
    out = []
    page = ''
    carry = []
    start = ''
    for ln in open(os.path.join(DATA, fn)):
        ln = ln.rstrip('\n')
        if ln.startswith('#') or not ln.strip():
            continue
        if ln.startswith('@'):
            page = ln[1:]
            continue
        for tok in re.findall(r'\{[^}]*\}|[^\s{}]+', ln):
            if tok.startswith('{'):
                if carry:
                    out.append((start, 'c', carry))
                    carry = []
                out.append((page, 'p', tok[1:-1]))
                continue
            cont = tok.endswith(',')
            if not carry:
                start = page
            carry = carry + [x for x in tok.split(',') if x and not x.startswith('~')]
            if not cont:
                out.append((start, 'c', carry))
                carry = []
    return out


def key():
    K = {}
    for ln in open(os.path.join(DATA, 'key.txt')):
        ln = ln.split('#')[0].split()
        if len(ln) >= 2:
            K[ln[0]] = ln[1]
    return K


def reading():
    R = {}
    for ln in open(os.path.join(DATA, 'reading.txt')):
        if ln.startswith('#') or not ln.strip():
            continue
        i, rest = ln.rstrip('\n').split(' ', 1)
        R[int(i)] = rest
    return R
