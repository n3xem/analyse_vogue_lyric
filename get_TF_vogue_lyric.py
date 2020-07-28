import json
from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.tokenfilter import POSStopFilter
from sklearn.feature_extraction.text import CountVectorizer


def calc_tf(w_idx, musicLyricJson):
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
with open('./music_lyric.json') as f:
    musicLyricJson = json.load(f)

for i in musicLyricJson.keys():
    lyric = musicLyricJson[i]["lyric"]
    tokens = analyzer.analyze(lyric)
    musicLyricJson[i]["wakati"] = ' '.join([t.surface for t in tokens])

X = vectorizer.fit_transform([musicLyricJson[i]["wakati"]
                              for i in musicLyricJson.keys()])
for i, bow in enumerate(X.toarray()):
    musicLyricJson[str(i)]["bow"] = bow


n = 2
WORDS = vectorizer.get_feature_names()

'''
for w_idx, count in enumerate(musicLyricJson[str(0)]["bow"]):
    if count >= n:
        print("{}\t{}: WORDS[{}]".format(count, WORDS[w_idx], w_idx))
'''

index = 0
sample_tfs = [calc_tf(w_idx, musicLyricJson)
              for w_idx, word in enumerate(WORDS)]
tfs_sorted = sorted(enumerate(sample_tfs), key=lambda x: x[1], reverse=True)

for i, tf in tfs_sorted[:30]:
    print("{}\t{}".format(WORDS[i], round(tf, 4)))
