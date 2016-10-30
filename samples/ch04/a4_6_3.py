# -*- coding: utf-8 -*-
#
# 二分搜索，递归


def binary_search_recursive(data, t, low, high):
    """ 递归的二分搜索 """

    # 终止条件
    if low > high:
        return None
    middle = (high - low) // 2 + low
    # 找到数据
    if data[middle] == t:
        return middle
    elif data[middle] > t:
        high = middle - 1
    elif data[middle] < t:
        low = middle + 1
    # 递归查找
    return binary_search_recursive(data, t, low, high)


def test_search():
    import random

    data = [i for i in range(1000)]
    x = random.randint(0, 999)

    k = binary_search_recursive(data, x, 0, 999)
    assert x == k

    k = binary_search_recursive(data, 1000, 0, 999)
    assert k is None

    k = binary_search_recursive(data, 1, 0, 999)
    assert k == 1

    k = binary_search_recursive(data, 999, 0, 999)
    assert k == 999
