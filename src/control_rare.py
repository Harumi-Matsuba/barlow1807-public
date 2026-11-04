"""⑤ 出現12回以下の記号の値だけをかき混ぜる対照（1000回）。指標は control.py と同じ。"""
import collections, random
from control import score, K, W, LETTERS
C = collections.Counter(s for w in W for s in w)
RARE = [s for s in LETTERS if C[s] <= 12]
r = random.Random(1807); vals = [K[s] for s in RARE]; res = []
for i in range(1000):
    v = vals[:]; r.shuffle(v); K2 = dict(K); K2.update(zip(RARE, v)); res.append(score(K2))
real = score(K)
print('記号', len(RARE), '本物', real, '平均', round(sum(res) / len(res), 1), '最大', max(res), '本物以上', sum(x >= real for x in res), '/ 1000')
