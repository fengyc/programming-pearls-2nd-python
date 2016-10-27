# -*- coding:utf-8 -*-
#
# 交换非相邻的内存 abc -> cba


def reverse(data, start, end):
    """ 进行取反

    :param data: 待取反的列表
    :param start: 开始下标
    :param end: 结束下标
    """
    for i in range((end - start + 1) // 2):
        temp = data[start + i]
        data[start + i] = data[end - i]
        data[end - i] = temp


def rotate(data, m, n):
    """ 进行旋转

    :param data: 数组
    :param m: a 段 m 个
    :param n: b 段 n 个
    """
    reverse(data, 0, m - 1)             # 翻转 a
    reverse(data, m, len(data) - 1)     # 翻转 bc
    reverse(data, 0, len(data) - 1)     # 整体翻转 -> bca

    reverse(data, 0, n - 1)                 # 翻转 b
    reverse(data, n, len(data) - m - 1)     # 翻转 c
    reverse(data, 0, len(data) - m - 1)     # 整体翻转 -> cba


def test_rotate():
    data = [i for i in range(10)]
    rotate(data, 2, 3)
    assert data == [5, 6, 7, 8, 9, 2, 3, 4, 0, 1]
