"""手紙の全文：平文の部分と、数字の語の読みをつないで出す。{平文} はそのまま、読みは小文字、? は [?語]、符号は [語]。"""
import os
from lib import load, reading, DATA
R = reading()
def word(r):
    if r in ('-', '='): return ''
    if r.startswith('#'):
        return '[' + r[1:] + ']'
    return ' '.join('[?' + x[1:] + ']' if x.startswith('?') else x for x in r.split())
out = []; cur = None; n = -1; buf = []
for p, k, v in load():
    if p != cur:
        if buf: out.append(' '.join(buf)); buf = []
        out.append('@' + p); cur = p
    if k == 'p':
        buf.append(v)
    else:
        n += 1
        w = word(R[n])
        if w: buf.append('«' + w + '»')
if buf: out.append(' '.join(buf))
t = '\n'.join(out).replace('» «', ' ').replace('= ', '').replace('=', '')
open(os.path.join(DATA, 'fulltext.txt'), 'w').write(t + '\n')
print(t)
