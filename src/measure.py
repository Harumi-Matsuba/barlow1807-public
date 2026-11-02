"""意味の通る割合を reading.txt から測る（語の単位と記号の単位の両方）。
語として通る＝鍵で読んだ字（詰め物を除く）が、読みの語の綴りの部分列になり、読みの語が英語の語である（母音を省く書き方なので部分列で比べる）。
数えない：? の語、# の符号、- の詰め物だけの語。= は前の語につなぐ。10 は語末の詰め物に使われるので、読み飛ばしてよい。"""
import collections, os, re
from wordfreq import zipf_frequency
from lib import load, key, reading, DATA
K = key()
W = [v for p, k, v in load() if k == 'c']
R = reading()
assert len(R) == len(W), (len(R), len(W))
def uni(x):
    """当時の表どおり u と v、i と j を同じ字とする（84＝u が gouernment に、89＝v が ovr に使われる）。"""
    return x.replace('v', 'u').replace('j', 'i')
NULLABLE = {'10', '12'}  # 語の頭と尻で値なしに使われる（hasd、tod、thand、dto）。12 は and の d にも使う
ALT = {'19': 'ae', '56': 'yw'}  # 19 は a：facility・adverse、e：empire・meditates。56 は y：duty・piety、w：what・with
def subseq(syms, target):
    """記号の並びが target の部分列か。10 と 12 は飛ばしてよい。同じ字が続くのは1字に数える（autthrty、sscvlativ）。"""
    t = uni(target)
    if any(s not in K for s in syms):
        return False
    seq = [(s, ALT.get(s, uni(K[s]))) for s in syms if K[s] != '·' and not K[s].startswith('[')]
    def go(i, pos, last):
        if i == len(seq):
            return True
        s, vs = seq[i]
        for v in vs:
            if v == last and go(i + 1, pos, last):
                return True
            f = t.find(v, pos)
            if f >= 0 and go(i + 1, f + 1, v):
                return True
        return s in NULLABLE and go(i + 1, pos, last)
    return go(0, 0, '')
DICT = {x.strip().lower() for x in open('/usr/share/dict/words')}
EXTRA = {'revd', 'buchanan', 'mussulmans', 'irremidiable', 'judgement', 'chimerical'}  # 綴りは手紙の平文に合わせた
import itertools
def badsyms(syms, t):
    """語の単位で通らない語で、取り除くと通る記号の最少の数を返す（2個まで）。語の3分の1を超えるなら None（語を読めていないとみる）。"""
    live = [k for k, s in enumerate(syms) if K.get(s) != '·']
    for n in (1, 2):
        if n * 3 > len(live):
            return None
        for c in itertools.combinations(live, n):
            if subseq([s for k, s in enumerate(syms) if k not in c], t):
                return n
    return None
tot = ok = skip = nul = 0; bad = []; slip = 0; whole = 0
i = 0
while i < len(W):
    syms = list(W[i]); r = R[i]; j = i + 1
    while j < len(W) and R[j] == '=':
        syms += W[j]; j += 1
    n = len(syms); tot += n
    if r == '-':
        nul += n
    elif r.startswith('#') or '?' in r:
        skip += n
    else:
        t = r.replace(' ', '')
        words_ok = all(zipf_frequency(x, 'en') > 0 or x in DICT or x in EXTRA or x[:-1] in DICT for x in r.split())
        if subseq(syms, t) and words_ok:
            ok += n
        else:
            n1 = badsyms(syms, t) if words_ok else None
            if n1 is None: whole += n
            else: slip += n1
            bad.append((i, r, ''.join(K.get(s, '?') for s in syms).replace('·', ''), ','.join(syms), '誤字の記号' if n1 else '語全体', n1 or n))
    i = j
den = tot - nul
print(f'記号 {tot}、詰め物だけの語 {nul}、対象 {den}、通る {ok}（{100 * ok / den:.1f}%）、不確か・符号 {skip}（{100 * skip / den:.1f}%）、通らない {den - ok - skip}（{100 * (den - ok - skip) / den:.1f}%）')
print(f'記号の単位（誤字の記号だけを通らないに数える）：通る {den - skip - slip - whole}（{100 * (den - skip - slip - whole) / den:.1f}%）、不確か・符号 {skip}、誤字の記号 {slip}、語全体が通らない {whole}')
for b in bad:
    print(*b)
