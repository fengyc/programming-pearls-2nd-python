# -*- coding:utf-8 -*-
#
# 向量向左旋转


def reverse(array, start, end):
    """ 进行取反

    :param array: 待取反的列表
    :param start: 开始下标
    :param end: 结束下标
    """
    for i in range((end - start + 1) // 2):
        temp = array[start + i]
        array[start + i] = array[end - i]
        array[end - i] = temp


def rotate(array, m):
    """ 进行旋转

    :param array: 数组
    :param m: 左分段结束下标
    """
    reverse(array, 0, m)
    reverse(array, m + 1, len(array) - 1)
    reverse(array, 0, len(array) - 1)


def test_rotate():
    array = [i for i in range(10)]
    rotate(array, 3)
    assert array == [4, 5, 6, 7, 8, 9, 0, 1, 2, 3]
