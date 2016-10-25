# -*- coding: utf-8 -*-
#
# 在 40 亿随机排序的 32 位整数的文件中，找到一个不在文件中的 32 位整数
#
# 不缺内存时，直接用位图表示，共用 2^32 / 8 共 512 MB 内存，然后在位图中搜索为 0 的位置
# 有限内存时，使用文件辅助进行二分搜索：
# 1. 按最高位为 0/1 划分为两个文件 f0 和 f1，则分别的范围为 [0,2^31)，[2^31，2^32)，
# 数据的个数为 c0 和 c1
# 2. 若 c0 < 2^31 ，则缺少的数在 f0，否则在 f1
# 3. 对在步骤 2 中得到的文件继续进行下一位的划分，直到能在内存中装下这个文件
#
# 假设只有 300 字节的内存，可装 75 个 32 位整数，需要划分文件 32-6=24 次
# 为充分利用内存，可将文件二分改为 32 / 64 / 128 (2^k)，以更加快速地收敛，并减少 IO

import uuid
import os

MEM_SIZE = 300


def search_missing_in_memory(array, start, end):
    array.sort()
    prev = array[0]
    for i in range(1, len(array)):
        if array[i] != prev + 1:
            return array[i]
    return None


def search_missing(input_file, k, l=0):
    """ 在无重复的输入文件中查找缺少的整数

    :param input_file: 输入文件路径
    :param k: 划分为 2^k 等分
    :param l: 当前划分搜索层次
    :return:
    """
    # 本次划分的每个区间的大小，区间的开始、结束
    interval = 1 << (32 - k * (l + 1))
    start =

    # 如果已能在内存中排序，那么执行内存排序和查找
    if interval <= MEM_SIZE:
        array = []
        with open(input_file, 'r') as fd:
            while True:
                line = fd.readline()
                if not line:
                    break
                    array.append(int(line.strip()))
        result = search_missing_in_memory(array)
        return result

    # 需要进行文件划分
    # 生成的临时文件名，共 1 << k 个
    temp_files = dict((i, uuid.uuid4().hex) for i in range(1 << k))
    # 临时文件的计数
    counts = dict((i, 0) for i in range(1 << k))
    # 临时文件对应的 fd
    temp_fds = dict((i, open(temp_files[i], 'w')) for i in range(1 << k))

    # 开始进行划分
    with open(input_file, 'r') as input_fd:
        while True:
            line = input_fd.readline()
            if not line:
                break
            num = int(line.strip())
            mask = ((1 << k) - 1) << 32 - k * l
            selected_fd = temp_fds[num & mask]
            selected_fd.write('%d\n', num)
            counts[num & mask] += 1
    for fd in temp_fds.values():
        fd.close()

    # 计数确定缺少的整数落在那个区间，应从小到大计算
    missing = None
    for i, c in counts:
        if c < interval:
            missing = i
            break
    # 清理临时文件
    for i, temp_file in temp_files:
        if i != missing:
            os.remove(temp_file)
    # 下一轮迭代查找
    return search_missing(temp_files[i], k, l + 1)


def test_search_missing():
    import random

    # 生成数据，10000 个整数
    data = []
    for i in range(10000):
        data.append(i)
    for i in range(10000):
        r = random.randint(0, 10000)
        temp = data[i]
        data[i] = data[r]
        data[r] = temp
    # 去掉任意一个
    r = random.randint(0, 10000)
    missing_value = data[r]
    del data[r]
    # 保存到输入文件
    with open('input.txt', 'w') as fd:
        fd.writelines(('%d\n' % num for num in data))

    # 进行搜索
    result = search_missing('input.txt', 2)

    assert result == missing_value

