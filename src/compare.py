"""Compare this transcription and key with the WAINUT reading in dbourdeau/cyphersolver, targets/barlow1807.
Usage: compare.py <path to targets/barlow1807>. Writes docs/comparison_transcription.tsv and docs/comparison_reading.tsv."""
import contextlib
import difflib
import glob
import io
import os
import re
import sys

from agreement import PAGES, first, norm, second
from lib import DATA, key

DOCS = os.path.join(DATA, '..', 'docs')


def their_signs(fn):
    t = re.sub(r'\{[^}]*\}', ' ', open(fn).read())
    out = []
    for run in re.findall(r'\d+(?:[,.]\s*\d+)*', t):
        for x in re.findall(r'\d+', run):
            out += norm(x)
    return out


def transcription(W):
    K = key()
    P = first()
    T = M = V = 0
    rows = [('page', 'this_repo', 'wainut')]
    for p in PAGES:
        x = P[p]
        y = their_signs(glob.glob(f'{W}/trans_final/{p}.txt')[0])
        n = max(len(x), len(y))
        sm = difflib.SequenceMatcher(None, x, y, autojunk=False)
        m = sum(b.size for b in sm.get_matching_blocks())
        v = sum(b.size for b in difflib.SequenceMatcher(None, [K.get(s, s) for s in x], [K.get(s, s) for s in y], autojunk=False).get_matching_blocks())
        print(p, 'names', round(100 * m / n, 1), 'values', round(100 * v / n, 1))
        T += n
        M += m
        V += v
        for t, i, j, k, l in sm.get_opcodes():
            if t != 'equal':
                rows.append((p, ','.join(x[i:j]), ','.join(y[k:l])))
    print('all names %.1f values %.1f (of %d); differences %d' % (100 * M / T, 100 * V / T, T, len(rows) - 1))
    open(os.path.join(DOCS, 'comparison_transcription.tsv'), 'w').write(''.join('\t'.join(r) + '\n' for r in rows))


def against_second(W):
    """Agreement of both transcriptions with the second readers, and whom they side with at one-to-one differences."""
    K = key()
    P = first()
    th = {p: their_signs(f'{W}/trans_final/{p}.txt') for p in PAGES}
    for who in ('sonnet', 'codex'):
        res = []
        for get in (P, th):
            T = V = 0
            for p in PAGES:
                x, y = get[p], second(p, who)
                T += max(len(x), len(y))
                V += sum(b.size for b in difflib.SequenceMatcher(None, [K.get(s, s) for s in x], [K.get(s, s) for s in y], autojunk=False).get_matching_blocks())
            res.append('%.1f (of %d)' % (100 * V / T, T))
        here = there = neither = 0
        for p in PAGES:
            x, y, z = P[p], th[p], second(p, who)
            mp = {}
            for t, i, j, k, l in difflib.SequenceMatcher(None, x, z, autojunk=False).get_opcodes():
                if t in ('equal', 'replace') and j - i == l - k:
                    mp.update({i + d: z[k + d] for d in range(j - i)})
            for t, i, j, k, l in difflib.SequenceMatcher(None, x, y, autojunk=False).get_opcodes():
                if t == 'replace' and j - i == l - k:
                    for d in range(j - i):
                        r = mp.get(i + d)
                        here += r == x[i + d]
                        there += r == y[k + d]
                        neither += r != x[i + d] and r != y[k + d]
        print(who, 'values: here', res[0], 'wainut', res[1], '; sides with here', here, 'wainut', there, 'neither', neither)


def word_counts():
    """Cipher words here: read, not fitting, uncertain (codes and nulls excluded)."""
    with contextlib.redirect_stdout(io.StringIO()):
        import measure as m
    bad = {b[0] for b in m.bad}
    ok = no = un = 0
    i = 0
    while i < len(m.W):
        j = i + 1
        while j < len(m.W) and m.R[j] == '=':
            j += 1
        r = m.R[i]
        if r != '-' and not r.startswith('#'):
            if '?' in r:
                un += 1
            elif i in bad:
                no += 1
            else:
                ok += 1
        i = j
    print('cipher words here: read', ok, 'not fitting', no, 'uncertain', un, 'of', ok + no + un)


def compare_key(W):
    K = key()
    KW = {}
    for ln in open(W + '/key_final.txt'):
        m = re.match(r'(\d+)=(\S*)', ln.strip())
        if m:
            KW[m.group(1)] = m.group(2)
    same = 0
    diff = []
    for s in set(K) & set(KW):
        a, b = K[s], KW[s]
        if a == '·' or a.startswith('['):
            continue
        if a == b or {a, b} <= {'u', 'v'} or {a, b} <= {'i', 'j'}:
            same += 1
        else:
            diff.append((s, a, b))
    print('key: same', same, 'different', len(diff), sorted(diff, key=lambda d: int(d[0])))


def words(t):
    return [w.lower().replace('v', 'u').replace('j', 'i') for w in re.findall(r"\[\??[^\]]*\]|[A-Za-z']+", t)]


def reading_text(W):
    A = {}
    cur = None
    for ln in open(os.path.join(DATA, 'fulltext.txt')):
        if ln.startswith('@'):
            cur = ln[1:].strip()
            A[cur] = []
        elif cur:
            A[cur] += words(re.sub(r'-\s+-', '', re.sub(r'[«»]', ' ', ln)))
    B = {}
    cur = None
    for ln in open(W + '/reading_12feb1807.md'):
        m = re.match(r'## Image (\d+)', ln)
        if m:
            cur = 'p%02d' % int(m.group(1))
        elif ln.startswith('## '):
            cur = None
        elif cur and ln.startswith('>'):
            B[cur] = words(re.sub(r'\[code \d+\]', '[code]', ln[1:]))
    rows = [('page', 'this_repo', 'wainut')]
    for p in PAGES:
        for t, i, j, k, l in difflib.SequenceMatcher(None, A[p], B[p], autojunk=False).get_opcodes():
            x, y = ' '.join(A[p][i:j]), ' '.join(B[p][k:l])
            if t != 'equal' and x.replace(' ', '') != y.replace(' ', ''):
                rows.append((p, x, y))
    only_w = sum('[?' in r[2] and '[?' not in r[1] for r in rows[1:])
    only_t = sum('[?' in r[1] and '[?' not in r[2] for r in rows[1:])
    print('reading: places', len(rows) - 1, 'marked ? only by WAINUT', only_w, 'only here', only_t)
    open(os.path.join(DOCS, 'comparison_reading.tsv'), 'w').write(''.join('\t'.join(r) + '\n' for r in rows))


if __name__ == '__main__':
    transcription(sys.argv[1])
    against_second(sys.argv[1])
    word_counts()
    compare_key(sys.argv[1])
    reading_text(sys.argv[1])
