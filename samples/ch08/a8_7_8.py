# -*- coding:utf-8 -*-
#
# 引入 ll 和 rr 变量，分别标记中间往左和中间往右的最大子向量的边界

from .a8_1 import maxsum3, maxsum4

def maxsum3_2(data, l, u):
    """分治"""
    if l > u:
        return 0
    if l == u:
        return max(0, data[l])
    m = (u-l) // 2 + l
    # 从中间往左的最大总和
    lmax = sum = 0
    ll = m
    for i in range(m, l-1, -1):
        sum += data[i]
        if sum >= lmax:
            ll = i
            lmax = sum
    # 从中间往右的最大总和
    rmax = sum = 0
    rr = m+1
    for i in range(m+1, u+1):
        sum += data[i]
        if sum >= rmax:
            rr = i
            rmax = sum
    # 递归计算
    return max(lmax+rmax, maxsum3(data, l, ll-1), maxsum3(data, rr+1, u))


def test_find_max():
    import datetime
    import random

    N = 10000
    data = [random.randint(0, 10) for x in range(N)]
    plan = [0 for x in range(N)]
    now_1 = datetime.datetime.now()
    m1 = maxsum3(data, 0, N - 1)
    now_2 = datetime.datetime.now()
    m2 = maxsum3_2(data, 0, N-1)
    now_3 = datetime.datetime.now()
    m3 = maxsum4(data, 0, N-1)
    now_4 = datetime.datetime.now()

    print("Maxsum3: %s, time: %s" % (m1, (now_2 - now_1).total_seconds()))
    print("Maxsum3_2: %s, time: %s" % (m2, (now_3 - now_2).total_seconds()))
    print("Maxsum4: %s, time: %s" % (m3, (now_4 - now_3).total_seconds()))