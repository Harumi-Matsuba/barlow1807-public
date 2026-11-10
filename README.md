# Sir George Barlow から Thomas Grenville への暗号の手紙（1807年）

Fort William、1807年2月12日付。「Private and Confidential」「Quadruplicate」。Cleveland Public Library、John G. White Collection（棚 W q091.92-B249t2）。
手紙の中の数字の部分の鍵を割り出し、全19ページを読んだ記録である。

**先行との関係：再現（reproduced）。** 同じ手紙は WAINUT が先に公開している（[dbourdeau/cyphersolver#231](https://github.com/dbourdeau/cyphersolver/issues/231)、2026年11月3日、read in part）。この読みは、それを見ずに作った別の読みで、先方を読んだ後に書き起こし・鍵・読みは変えていない。新しい点は p03 の読み、先方の穴の語の読みなどである。比較は `docs/COMPARISON.md`。

**状態：全文の読み。** 暗号の記号 3,869 のうち、読みが語として通るものは 3,722（**96.2%**、記号の単位）。
**語の単位の厳しい数え方では 3,535（91.4%）で、95% に届かない。** 違いは、1語の中の1記号が合わない語（書き手の誤りとみられる語が28語）の扱いである。
数え方は下の「数字」に書いた。この記号の単位の数え方は、語の単位の結果を見た後に採ったものなので、両方を並べて読んでほしい。

## 読めたこと

Claudius Buchanan の *Memoir of the Expediency of an Ecclesiastical Establishment for British India* が勧める、インドの教会設立案への反対意見である。Barlow は次のように書く。

- インド人の信仰への寛容は「our eastern empire」の「main foundation」である。
- 政府が改宗を企てているという懸念が広がれば、法で約束した不干渉が破られ、帝国の土台が危うくなる。
- 「the coast」の「native troops」が最近抱いた懸念（1806年の Vellore の反乱を指すとみる。これは手紙の中に書かれておらず、こちらの推定）は、教会の設立で裏づけられたことになる。
- 政府は、Fort William のカレッジ（符号 4845 からの推定）で宗教を論じることを抑えてきた。
- 在インドの共同体の宗教的な利益は、人物の確かな聖職者を置くことで足りる。

全文は `data/fulltext.txt`、説明は `docs/READING.md`。

## 方式

英文の中で、語の一部を2桁の数字に換える同音換字である。語の切れ目は点で、母音は省くことが多い（govt、mnstrs）。
1つの字に複数の数字があり（t＝44・77・50、n＝90・70・83 など）、値のない数字もある（11・20・21・22・2・1・100・1100・2200。10・12 も値なしに使うことがある）。
4桁の 4990・5650・4845 は語の符号で、値は文脈からの推定（India、British、Fort William）。4087・5089・4600 は値が分からない。
記号の表は `data/key.tsv`。

## 数字

| 項目 | 値 |
|---|---|
| 暗号の記号（詰め物だけの語を除く） | 3,869（語 703、全19ページ） |
| 語として通る（記号の単位。誤字の記号だけを通らないに数える） | 3,722（96.2%）。誤字の記号 29、語全体が読めない 6、不確か・符号 112（2.9%） |
| 語として通る（語の単位。語の中の1記号でも合わなければ語全体を通らないに数える） | 3,535（91.4%）。通らない 222（5.7%）、不確か・符号 112（2.9%） |
| 対照（字の値のかき混ぜ1000回） | 本物以上 0 回（語のうち骨組みが英語の語と同じもの：本物 517/703、かき混ぜの平均 244.3、最大 367） |
| 対照（出現12回以下の32記号の値だけをかき混ぜ1000回） | 本物以上 0 回（本物 517、平均 474.2、最大 493） |
| 別の読み手との一致（値） | Claude Sonnet 19ページ 93.5%（ページの最低は p16 の 88.7%）。OpenAI Codex 19ページ 91.0%（1回目を直す前）、91.4%（直した後。ページの最低は p12 の 83.5%） |
| 較正 | なし（当時の解読文も刊本も見つからない） |

どちらの数字にも緩めた扱いがある（u=v、i=j、同じ字の連続は1字、10・12 は読み飛ばしてよい、19 は a か e、56 は y か w）。一部は読みを作った後に足した。`docs/METHOD.md` に全部書いた。

## 人の確認

**人はこの書き起こしを確かめていない。** 書き起こしも読みも AI が行った。AI どうしの一致は、人の確認の代わりにならない。

## 先行との関係

先行は WAINUT の読みである（上の冒頭、`docs/COMPARISON.md`、`docs/PRIOR_CHECK.md`）。「初めて解いた」とは言わない。Grenville 文書の原本、Barlow 文書、刊本の一部は見ていない。

## AI の使用

資料の取得、書き起こし、鍵の割り出し、対照、この文書の作成は AI（Anthropic Claude）が行った。
2回目は Claude Sonnet と OpenAI Codex（codex-cli 0.163.0-alpha.10.2、gpt-6-astra、推論 high）が、1回目も鍵も見ずに画像だけから読んだ。
人が行ったのは、作業の指示と公開の判断である。

## 更新履歴
- 2026-11-11：先行の読み（WAINUT）との書き起こしの食い違い75か所を画像で判定し、WAINUT が支持された1対1の14か所を直した。語として通る割合 96.3% → 96.2%（記号の単位）、92.4% → 91.4%（語の単位）。読みの語は変えていない。詳細は `docs/COMPARISON.md` の「画像での判定」。

## 中身

- `data/tr1.txt` 書き起こし（直した後）。`data/tr1_before_corrections.txt` 直す前。
- `data/key.txt`・`data/key.tsv` 鍵。`data/reading.txt` 語ごとの読み。`data/fulltext.txt` 全文。
- `data/image_check.tsv` 画像の2択の問いと答えの全部。
- `second/` 2回目の読み（Sonnet、Codex）と依頼文。
- `src/` 計測のプログラム（`python3 src/measure.py`、`src/control.py`、`src/agreement.py sonnet`、`src/compare.py`）。測るには `pip install wordfreq` が要る。
- `docs/` METHOD（方法と限界）、OPEN（未解決）、READING（読み）、COMPARISON（先行との比較）、PRIOR_CHECK（先行の調べ）。
- `SOURCES.md` 資料とページの順。

英語版は `*.en.md`。
