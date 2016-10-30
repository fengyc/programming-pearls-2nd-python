# -*- coding: utf-8 -*-
#
# 搜索距离点 (x0,y0) 最近的线段
#
# 线段用系数表示为 (ai,bi)，在 y 方向上升序排序，利用类似二分搜索的方法，或者先计算距离
# 然后排序都可以实现，这里用二分搜索的方法
#
# 注意：中止条件为 high - low <= 1
# 原问题的表述对点在线段上、点在最下方、点在最上方等特殊情况没有说明，这里加上的补充为：
# （1）返回值为包围点的下方和上方线段下标的元组
# （2）在最上方时，返回最上方线段和 None 的元组
# （3）在最下方时，返回 None 和最下方的元组
# （4）在线段上时，则上下方都为该线段的下标
# 小心处理点在线段上的情况


def dist(data, index, t):
    """ 计算点与线段的 y 方向上的距离 """
    return t[1] - (data[index][0] * t[0] + data[index][1])


def binary_search(data, t):
    """ 使用二分法进行查找与点 t 最近的两个线段 """
    low = 0
    high = len(data) - 1
    # 点在最下面
    dl = dist(data, low, t)
    if dl < 0:
        return None, low
    if dl == 0:
        return low, low
    # 在最上面
    dh = dist(data, high, t)
    if dh > 0:
        return high, None
    if dh == 0:
        return high, high
    # 其它情况
    while high - low > 1:
        middle = (high - low) // 2 + low
        d = dist(data, middle, t)
        if d > 0:
            low = middle
        elif d < 0:
            high = middle
        else:
            low = high = middle
    return low, high


def test_search():
    data = [(0, 1), (1, 1), (0, 2), (-1, 3), (0, 3), (1, 3)]

    t = (0.5, 2)
    assert binary_search(data, t) == (2, 2)

    t = (0.5, 0)
    assert binary_search(data, t) == (None, 0)

    t = (0.5, 4)
    assert binary_search(data, t) == (5, None)

    t = (0.5, 3.5)
    assert binary_search(data, t) == (5, 5)

    t = (0.5, 1)
    assert binary_search(data, t) == (0, 0)

    t = (0.5, 2.2)
    assert binary_search(data, t) == (2, 3)
