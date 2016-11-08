# -*- coding:utf-8 -*-
#
# 计算连续子向量的最大和
#
# 基本思路：
# 这个题目要求计算一个数组中若干连续子向量中，由于中间存在重复的数据，可用
# 中间数组保存，从而让复杂度降低为 O(n^2)
#
# 分治方法是把数组切分为 a b 两部分，那么最大和可能在a、b或者跨ab。当它跨ab
# 时，必然包含中间的数值，则可能从中间数据分别往左往右计算连续的最大值，然后相加。
# 分治的方法避免了检测所有子向量，得到的时间复杂度为 O(n*log(n))
#
# 扫描方法是对前i-1个元素，记录其总和最大的子向量。那么加入i时，要么然后为前面
# 的最大子向量，或最大子向量的结束位置调整为i。它的时间复杂度为 O(n) !!!!!
#
# 10000 个数的运行时间分别为 15.032368，0.055864，0.004329


def maxsum(data, l, u):
    """存储中间数据"""
    sums = [0 for i in range(l, u+1)]
    max_all = 0
    for i in range(l, u+1):
        for j in range(l, u-i + 1):
            sums[j] = sums[j] + data[j+i]
        max_cur = max((sums[x] for x in range(l, u-i+1)))
        if max_cur > max_all:
            max_all = max_cur
    return max_all


def maxsum3(data, l, u):
    """分治"""
    if l > u:
        return 0
    if l == u:
        return max(0, data[l])
    m = (u-l) // 2 + l
    # 从中间往左的最大总和
    lmax = sum = 0
    for i in range(m, l-1, -1):
        sum += data[i]
        lmax = max(lmax, sum)
    # 从中间往右的最大总和
    rmax = sum = 0
    for i in range(m+1, u+1):
        sum += data[i]
        rmax = max(rmax, sum)
    # 递归计算
    return max(lmax+rmax, maxsum3(data, l, m), maxsum3(data, m+1, u))


def maxsum4(data, l, u):
    """扫描"""
    maxsofar = 0        # 目前最大总和
    maxendinghere = 0   # 最大子向量的开始到目前下标的总和
    for i in range(l, u+1):
        maxendinghere = max(maxendinghere + data[i], 0)
        maxsofar = max(maxsofar, maxendinghere)
    return maxsofar


def test_find_max():
    import datetime
    import random

    N = 10000
    data = [random.randint(-99, 99) for x in range(N)]
    plan = [0 for x in range(N)]
    now_1 = datetime.datetime.now()
    m1 = maxsum(data, 0, N - 1)
    now_2 = datetime.datetime.now()
    m2 = maxsum3(data, 0, N-1)
    now_3 = datetime.datetime.now()
    m3 = maxsum4(data, 0, N-1)
    now_4 = datetime.datetime.now()

    print("Maxsum: %s, time: %s" % (m1, (now_2-now_1).total_seconds()))
    print("Maxsum3: %s, time: %s" % (m2, (now_3-now_2).total_seconds()))
    print("Maxsum4: %s, time: %s" % (m3, (now_4-now_3).total_seconds()))
