# -*- coding:utf-8 -*-
#
# 向量向左旋转


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


def rotate(data, m):
    """ 进行旋转

    :param data: 数组
    :param m: 前 m 个
    """
    reverse(data, 0, m - 1)
    reverse(data, m, len(data) - 1)
    reverse(data, 0, len(data) - 1)


def test_rotate():
    data = [i for i in range(10)]
    rotate(data, 4)
    assert data == [4, 5, 6, 7, 8, 9, 0, 1, 2, 3]
