# -*- coding: utf-8 -*-

from underthesea import word_tokenize
import numpy as np
import re

def clean_up(sentence):
    sentence_words = word_tokenize(sentence)
    sentence_words = [word.lower() for word in sentence_words]
    return sentence_words

# bag of words
def bow(sentence, words, show_details=False):
    sentence_words = clean_up(sentence)
    # bag of words
    bag = [0]*len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)

    return(np.array(bag))

# stop word
def stopWord():
    stop_words: []
    f = open("stopwords.txt", mode="r", encoding="utf-8")
    for temp in f:
        stop_words.append(temp.rstrip('\n'))
    f.close()

    return stop_words

# handle input
def handleInput(sentence):
    text_lower = sentence.lower()
    text_strip = text_lower.strip()
    text_whitespace = " ".join(text_strip.split())
    text = re.sub('[<>\/!@#$\|\$\%\^\&\*\_\-\=\_\~\`\+]', '', text_whitespace)
    
    return text