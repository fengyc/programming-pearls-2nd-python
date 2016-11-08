# -*- coding:utf-8 -*-
#
# 找到总和最接近 t 的子向量


def mindelta(data, t):
    sums = [0] # sums[i+1] = data[0]+...+data[i]
    # 初始化
    for i in range(1, len(data)+1):
        sums.append(data[i-1]+sums[i-1])
    print(sums)
    # 逐个计算最接近 t 的子向量
    m = abs(sums[0] - t)
    l = r = 0
    for i in range(0, len(sums)-1):
        for j in range(i+1, len(sums)):
            sumij = sums[j] - sums[i]
            delta = abs(sumij - t)
            if delta < m:
                if delta == 0:
                    print('0')
                m = delta
                l = i
                r = j
    return (l, r-1, m)


def test_mindelta():
    import random

    N = 10
    data = [random.randint(0, 1000) for x in range(N)]
    t = sum(data[3:8])
    print(t)
    print(data)
    r = mindelta(data, t)
    print(r)
