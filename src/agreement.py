"""Agreement of the first reading with a second reader, page by page. Usage: agreement.py sonnet|codex [data file]"""
import difflib
import os
import re
import sys

from lib import DATA, key
ROOT = os.path.join(DATA, '..')
PAGES = 'p15 p16 p17 p18 p01 p02 p03 p04 p05 p06 p07 p08 p09 p10 p11 p12 p13 p14 p19'.split()


def norm(tok):
    """The writer's closing point can look like 0 or 1 (190 for 19, 402 for 40): three digits keep the first two.
    Four digits are split in two, against a missed comma. Both readings get the same treatment."""
    if len(tok) == 3:
        return [tok[:2]]
    if len(tok) == 4:
        return [tok[:2], tok[2:]]
    return [tok]


def toks(t):
    t = re.sub(r'\{[^}]*\}', ' ', t)
    t = re.sub(r'~\d+', ' ', t)
    out = []
    for x in re.findall(r'\^?\d+(?:/\d+)*', t):
        out += norm(x.lstrip('^').split('/')[0])
    return out


def first(fn='tr1.txt'):
    P = {}
    cur = ''
    for ln in open(os.path.join(DATA, fn)):
        if ln.startswith('#'):
            continue
        if ln.startswith('@'):
            cur = ln[1:].strip()
            P[cur] = []
            continue
        P[cur] += toks(ln)
    return P


def second(p, who):
    out = []
    for b in '123':
        fn = os.path.join(ROOT, 'second', who, f'{p}_{b}.txt')
        if not os.path.exists(fn):
            return None
        s = toks(open(fn).read())
        best = 0
        for k in range(min(len(out), len(s), 45), 2, -1):
            if difflib.SequenceMatcher(None, out[-k:], s[:k], autojunk=False).ratio() >= 0.7:
                best = k
                break
        out += s[best:]
    return out


def main(who, fn='tr1.txt'):
    P = first(fn)
    K = key()
    T = M = V = 0
    for p in PAGES:
        y = second(p, who)
        if y is None:
            continue
        x = P[p]
        n = max(len(x), len(y))
        m = sum(b.size for b in difflib.SequenceMatcher(None, x, y, autojunk=False).get_matching_blocks())
        v = sum(b.size for b in difflib.SequenceMatcher(None, [K.get(s, s) for s in x], [K.get(s, s) for s in y], autojunk=False).get_matching_blocks())
        print(p, 'names', round(100 * m / n, 1), 'values', round(100 * v / n, 1))
        T += n
        M += m
        V += v
    print('all names %.1f values %.1f (of %d)' % (100 * M / T, 100 * V / T, T))
    return 100 * V / T


if __name__ == '__main__':
    main(*sys.argv[1:])
