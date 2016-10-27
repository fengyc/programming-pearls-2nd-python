# -*- coding:utf-8 -*-
#
# 通过直接计算的方式得到每个移位后的下标对应的原始下标
#
# 假设数组 s 长度为 n ，左移 k 位后的下标为 i ，那么有 i <- (i+k)%n
# 此时继续对移位到 i+k 位置，有 (i+k)%n <- (i+2k)%n ，这个过程直到重新回到需要
# 移动 i 的位置 (i+(a-1)k)%n <- (i+ak)%n = i ，即移动 a 次后完成一个移动循环，这时
# 如果 a < n ，则需要移动 i+1 、i+2、...、i+x-1，x 为移动循环的个数。
# 由 (i+ak)%n = i ，得到 ak % n = 0 ，那么 ak 为 k 的倍数也为 n 的倍数，ak 是 k 和 n
# 的最小公倍数 lcm(n,k)，a = lcm(n,k) / k，需要的移动循环个数 x = n/a ，替换 a 可得到
# x = n*k / lcm(n,k) 。
# 由于最大公约数和最小公倍数之间存在关系 n*k = lcm(n,k)*gcd(n,k)
# 那么 x = gcd(n,k)
# 最大公约数可用辗转相除法求


def gcd(a, b):
    """ 计算最大公约数 greatest common divisor

    使用辗转相除法求最大公约数
    """
    m = max(a, b)
    n = min(a, b)
    while n != 0:
        c = m % n
        m = n
        n = c
    return m


def lcm(a, b):
    """ 计算最小公倍数 lowest common multiple

    lcm = a*b / gcd(a,b)
    """
    c = gcd(a, b)
    return a * b // c


def rotate(data, k):
    n = len(data)
    x = gcd(n, k)
    for i in range(x):
        temp = data[i]
        j = 0
        while (i + (j + 1) * k) % n != i:
            data[(i + j * k) % n] = data[(i + (j + 1) * k) % n]
            j += 1
        data[(i + j * k) % n] = temp


def test_rotate():
    data = [i for i in range(10)]
    rotate(data, 3)
    assert data == [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]
