__author__ = 'ShubhamTripathi'

import string
from nltk.util import ngrams

def getresource():
    punct = set(string.punctuation)
    nums = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    num_string = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'hundred', 'thousand',
                  'lakh', 'million', 'billion']
    return punct, nums, num_string

def isAscii(utter):
    return all(ord(c) < 128 for c in utter)

def unpack(list):
    unpacked_list = []
    for i in list:
        unpacked_list += i
    return unpacked_list

def char_ngram(n, word):
    char_tokens = list(word)
    char_ngrams = ngrams(char_tokens, n)  # prefix-suffix is automatically generated here
    return map(lambda x: ''.join(x), char_ngrams)

def word_normalisation(word):
    norm_word = []
    for letter in word:
        if letter.isupper():
            norm_word.append('A')
        elif letter.islower():
            norm_word.append('a')
        elif letter.isdigit():
            norm_word.append(0)
        else:
            norm_word.append(letter)
    try:
        rword = "".join(norm_word)
    except:
        rword = "0000"
    return rword

