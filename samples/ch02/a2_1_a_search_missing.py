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
# 为充分利用内存，可将文件二分改为 32 / 64 / 128 (k分)，以更加快速地收敛，并减少 IO


import uuid
import os
import math

MEM_SIZE = 300


def search_missing_in_memory(array, start, end):
    """ 在内存中查找缺少的一个整数 """

    array.sort()
    prev = array[0]
    # 如果 array 中最小值不为 min，那么缺少了最小值
    if prev != start:
        return start
    # 查 array 中间是否缺少了某个数
    for i in range(1, len(array)):
        if array[i] != prev + 1:
            return prev + 1
        prev += 1
    # 查最后是否缺少了某个数
    if array[-1] < end:
        return array[-1] + 1
    # 没有找到缺少的数
    return None


def search_missing(input_file, start, end, k=2):
    """ 在无重复的输入文件中查找缺少的整数，输入文件的整数范围为 [start, end]

    :param input_file: 输入文件路径
    :param start: 范围开始
    :param end: 范围结束
    :param k: 划分为 k 等分
    :return:
    """
    # 如果已能在内存中排序，那么执行内存排序和查找
    if end - start + 1 <= MEM_SIZE:
        array = []
        with open(input_file, 'r') as fd:
            while True:
                line = fd.readline()
                if not line:
                    break
                array.append(int(line.strip()))
        result = search_missing_in_memory(array, start, end)
        return result

    # 分为 k 等分时，每段应该有 ceil((max - min + 1) / k) 个
    chunk_size = math.ceil((end - start + 1) / k)
    temp_files = [uuid.uuid4().hex for i in range(k)]   # 临时文件名
    temp_counts = [0 for i in range(k)]                 # 每段的计数
    temp_fds = [open(temp_files[i], 'w') for i in range(k)]
    # 开始进行划分
    with open(input_file, 'r') as input_fd:
        while True:
            line = input_fd.readline()
            if not line:
                break
            num = int(line.strip())
            idx = (num - start) // chunk_size
            temp_fds[idx].write('%d\n' % num)
            temp_counts[idx] += 1
    for fd in temp_fds:
        fd.close()
    # 计数确定缺少的整数落在那个区间，应从小到大计算
    missing = None
    for i in range(k):
        if temp_counts[i] < chunk_size:
            missing = i
            break
    # 清理临时文件
    for i in range(k):
        if i != missing:
            os.remove(temp_files[i])
    # 下一轮迭代查找
    if missing is not None:
        missing_start = start + missing * chunk_size
        missing_end = missing_start - 1 + chunk_size
        if missing_end > end:
            missing_end = end
        result = search_missing(temp_files[missing], missing_start,
                                missing_end, k)
        # 清理剩下的临时文件
        os.remove(temp_files[missing])
        return result
    return None


def test_search_missing():
    import random

    # 生成数据，10000 个整数
    data = [i for i in range(10000)]
    for i in range(10000):
        r = random.randint(0, 9999)
        temp = data[i]
        data[i] = data[r]
        data[r] = temp
    # 去掉任意一个
    r = random.randint(0, 9999)
    missing_value = data[r]
    del data[r]
    # 保存到输入文件
    with open('input.txt', 'w') as fd:
        fd.writelines(('%d\n' % num for num in data))

    # 进行搜索
    result = search_missing('input.txt', 0, 9999, 8)
    assert result == missing_value
