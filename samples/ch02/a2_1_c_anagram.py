# -*- coding:utf-8 -*-
#
# 变位词处理
#
# 将变位词排序，排序后的序列作为该词的 key，具有同一 key 的词为变位词


def search_anagrams(words):
    d = {}
    for word in words:
        key = ''.join(sorted(word))
        if d.get(key) is None:
            d[key] = []
        d[key].append(word)
    return d


def test_search_anagrams():
    words = ['pots', 'tops', 'stop']
    d = search_anagrams(words)
    assert d is not None
