import random
import json
import re
from janome.tokenizer import Tokenizer

N_SENTENCE = 20


def is_japanese(text):
    return True if re.search(r'[ぁ-んァ-ン]', text) else False


def wakati(text):
    t = Tokenizer()
    if is_japanese(text):
        text = text.replace('\n', '').replace('\r', '').replace(' ', '。')

        result = t.tokenize(text, wakati=True)
        return result
    else:
        return text.split()


def generate_text(n_sentence):
    with open('./music_lyric.json') as f:
        musicLyricJson = json.load(f)
        wordlist = []
        for i in musicLyricJson.keys():
            lyric = musicLyricJson[i]["lyric"]
            wordlist.extend(wakati(lyric))

        markov = {}
        w1 = ""
        w2 = ""
        for word in wordlist:
            if w1 and w2:
                if(w1, w2) not in markov:
                    markov[(w1, w2)] = []
                markov[(w1, w2)].append(word)
            w1, w2 = w2, word

        cnt_kuten = 0
        sentence = ""
        w1, w2 = random.choice(list(markov.keys()))
        while cnt_kuten < n_sentence:
            tmp = random.choice(markov[(w1, w2)])
            sentence += tmp
            if(tmp == '。' or tmp == '！' or tmp == '？'):
                cnt_kuten += 1
                sentence += '\n'
            w1, w2 = w2, tmp

        print(sentence)


generate_text(N_SENTENCE)
