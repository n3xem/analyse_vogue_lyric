import random
import json
import re
from janome.tokenizer import Tokenizer

N_SENTENCE = 20


def is_japanese(text):
    """引数が日本語がどうか判定する

    Parameters
    ----------
    text : string
        日本語かどうか判定する文字列

    Returns
    -----------
    bool
        日本語ならTrue,違うならFalse
    """
    return True if re.search(r'[ぁ-んァ-ン]', text) else False


def wakati(text):
    """引数に渡された文字列を分かち書きしてリストとして返す

    Parameters
    ----------
    text : string
        分かち書きの対象

    Returns
    ----------
    list
        分かち書きした単語のリスト
    """
    t = Tokenizer()
    if is_japanese(text):
        text = text.replace('\n', '').replace('\r', '').replace(' ', '。')

        result = t.tokenize(text, wakati=True)
        return result
    else:
        return text.split()


def generate_text(n_sentence):
    """引数の数の文がある歌詞を生成する

    Parameters
    ----------
    n_sentence : int
        文の数
    """
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

        # 文章の区切りの数
        cnt_kugiri = 0
        sentence = ""
        w1, w2 = random.choice(list(markov.keys()))
        while cnt_kugiri < n_sentence:
            tmp = random.choice(markov[(w1, w2)])
            sentence += tmp

            # 。か！が？が来たら文末だと判定する
            if(tmp == '。' or tmp == '！' or tmp == '？'):
                cnt_kugiri += 1
                sentence += '\n'
            w1, w2 = w2, tmp

        print(sentence)


generate_text(N_SENTENCE)
