import json
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.tokenfilter import POSStopFilter
from sklearn.feature_extraction.text import CountVectorizer


def calc_tf(w_idx, musicLyricJson):
    """WORD[w_idx]のTF値を算出する

    Parameters
    ----------
    w_idx : int
        TF値を求めたいwordのインデックス
    musicLyricJson : dictionary
        Jsonを辞書に直したもの

    Returns
    ----------
    float
        求めたTF値
    """

    word_count = 0
    for i in musicLyricJson.keys():
        word_count += musicLyricJson[i]["bow"][w_idx]

    if word_count == 0:
        return 0.0

    sum_of_words = 0
    for i in musicLyricJson.keys():
        sum_of_words += sum(musicLyricJson[i]["bow"])
    return word_count/float(sum_of_words)


tokenizer = Tokenizer()
vectorizer = CountVectorizer()
token_filters = [POSStopFilter(['記号', '助詞', '助動詞', '動詞'])]
analyzer = Analyzer(tokenizer=tokenizer, token_filters=token_filters)

# Jsonをロードして辞書に入れる
with open('./music_lyric.json') as f:
    musicLyricJson = json.load(f)

# 歌詞を分かち書きして辞書に保存する
for i in musicLyricJson.keys():
    lyric = musicLyricJson[i]["lyric"]
    tokens = analyzer.analyze(lyric)
    musicLyricJson[i]["wakati"] = ' '.join([t.surface for t in tokens])

# 歌詞のBoWを計算する
X = vectorizer.fit_transform([musicLyricJson[i]["wakati"]
                              for i in musicLyricJson.keys()])

# 計算したBowを辞書に保存する
for i, bow in enumerate(X.toarray()):
    musicLyricJson[str(i)]["bow"] = bow

# Bowのインデックスに対応する単語の情報を取得する
WORDS = vectorizer.get_feature_names()

# 各単語のTF値を取得する
lyrics_tfs = [calc_tf(w_idx, musicLyricJson)
              for w_idx, word in enumerate(WORDS)]

# TF値をソートする
tfs_sorted = sorted(enumerate(lyrics_tfs), key=lambda x: x[1], reverse=True)

# ソートしたTF値を上から30個分だけ出力する
for i, tf in tfs_sorted[:30]:
    print("{}\t{}".format(WORDS[i], round(tf, 4)))
