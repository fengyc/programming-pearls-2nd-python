# -*- coding:utf-8 -*-
#
# 递归计算


def calc(k, a, c, m):
    """ 递归计算

    :param k: k 阶
    :param a: 输入 a 数组
    :param c: 输入常数 c 数组
    :param m:
    :return: 数组 [a1, ..., am]
    """
    for i in range(k, m):
        x = 0
        for j in range(k):
            x += c[j] * a[i-j-1]
        x += c[k]
        a.append(x)
    return a[:m]


def test_calc():
    k = 2
    a = [2, 3]
    c = [1, 2, 3]
    m = 5
    assert calc(k, a, c, m) == [2, 3, 10, 19, 42]
    assert calc(k, a, c, 2) == [2, 3]
