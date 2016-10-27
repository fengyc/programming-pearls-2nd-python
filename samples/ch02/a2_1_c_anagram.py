# -*- coding:utf-8 -*-
#
# 变位词处理
#
# 将变位词按照字母排序，排序后的序列作为该词的标识 key，具有同一 key 的词为变位词
#
# 优化：标识方法中，可将相同的字母使用一个数字表示，如 spool 标记为 lo2ps


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
