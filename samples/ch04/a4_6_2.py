# -*- coding:utf-8 -*-
#
# 二分搜索，并返回第一个匹配的数据
#
# 输入数据 data 从小到大排序
#
# 关键在于对 data[middle] == t 时的处理，需要再次计算 low 与 middle 中间的值 data[q]
# 来确定下一步的调整：data[q] < t 时，low = q ； data[q] == t 时，height = q 。然后
# 继续查找 t ，直到第一次出现的位置。
#


def binary_search_first(data, t):
    n = len(data)
    low = 0
    height = len(data) - 1

    while low <= height:
        if data[low] == t:
            return low
        middle = (height - low) // 2 + low
        if data[middle] > t:
            height = middle - 1
        elif data[middle] < t:
            low = middle + 1
        else:
            q = (middle - low) // 2 + low
            if data[q] < t:
                low = q + 1
            else:
                height = q

    return None


def test_search():
    import random

    data = [i for i in range(1000)]
    x = random.randint(0, 999)
    for i in range(50):
        data.insert(x, x)

    k = binary_search_first(data, x)

    assert x == k