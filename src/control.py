"""対照：鍵の字の値をかき混ぜる（1000回）。指標は、数字の語のうち、子音の骨組みが英語の語（wordfreq 上位4万語）の骨組みと同じものの割合。
母音を省く書き方なので、綴りの完全一致でなく骨組みで比べる。詰め物（値なし）の記号はかき混ぜない。"""
import random, re
from wordfreq import top_n_list
from lib import load, key
def skel(s):
    return re.sub(r'[aeiouy]', '', s)
LEX = {skel(w) for w in top_n_list('en', 40000) if w.isalpha()}
LEX.discard('')
K = key()
W = [v for p, k, v in load() if k == 'c' and all(s in K for s in v)]
LETTERS = [s for s, v in K.items() if len(v) == 1 and v.isalpha()]
def score(K2):
    n = 0
    for w in W:
        t = ''.join(K2.get(s, '') for s in w).replace('·', '')
        if len(t) >= 2 and skel(t) in LEX:
            n += 1
    return n
real = score(K)
r = random.Random(1807)
vals = [K[s] for s in LETTERS]
res = []
for i in range(1000):
    v = vals[:]
    r.shuffle(v)
    K2 = dict(K)
    K2.update(zip(LETTERS, v))
    res.append(score(K2))
print('語', len(W), '本物', real, round(100 * real / len(W), 1), '%')
print('かき混ぜ 平均', round(sum(res) / len(res), 1), '最大', max(res), '本物以上', sum(x >= real for x in res), '/ 1000')
