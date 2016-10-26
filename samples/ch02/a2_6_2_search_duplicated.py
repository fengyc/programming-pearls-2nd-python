# -*- coding:utf-8 -*-
#
# 在大文件中搜索重复的一个整数
#
# 大文件分 k 段，每段包含的数据为 n/k 个，第 i 段范围为 [i*(n/k), (i+1)*(n/k)) ，若某
# 段长度超过 n/k 个，则重复的数据在该段内，对该段所在的文件继续划分，直到能在内存中能容下
# 所有的数字，进行内存搜索

import uuid
import math
import os

MEM_SIZE = 2000


def search_duplicated_in_memory(array):
    array.sort()
    for i in range(0, len(array) - 1):
        if array[i] == array[i+1]:
            return array[i]
    return None


def search_duplicated(input_file, start, end, k=2):
    """ 在文件中搜索重复的一个整数

    :param input_file: 输入文件
    :param start: 最小整数
    :param end: 最大整数
    :param k: 分 k 段
    """
    # 如果内存能容下此文件，直接内存搜索
    if end - start + 1 <= MEM_SIZE:
        data = []
        with open(input_file) as input_fd:
            while True:
                line = input_fd.readline()
                if not line:
                    break
                data.append(int(line.strip()))
        return search_duplicated_in_memory(data)

    # 划分文件
    chunk_size = math.ceil((end - start + 1) / k)   # 每个文件的长度
    temp_files = [uuid.uuid4().hex for i in range(k)]
    temp_fds = [open(temp_files[i], 'w') for i in range(k)]
    temp_counts = [0 for i in range(k)]
    with open(input_file) as input_fd:
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
    # 计数检查重复的整数落在哪个段
    duplicated = None
    for i in range(k):
        if temp_counts[i] > chunk_size:
            duplicated = i
            break
    # 清理中间文件
    for i in range(k):
        if i != duplicated:
            os.remove(temp_files[i])
    # 继续在这段内搜索
    duplicated_start = start + chunk_size * duplicated
    duplicated_end = start - 1 + chunk_size * (duplicated + 1)
    if duplicated_end > end:
        duplicated_end = end
    result = search_duplicated(temp_files[duplicated], duplicated_start,
                               duplicated_end, k)
    # 清理有重复数据的中间文件
    if duplicated is not None:
        os.remove(temp_files[duplicated])

    return result


def test_search_duplicated():
    import random

    # 生成输入文件
    data = [i for i in range(10000)]
    for i in range(10000):
        r = random.randint(0, 9999)
        temp = data[i]
        data[i] = data[r]
        data[r] = temp
    # 增加一个重复整数
    duplicated_value = random.randint(0, 9999)
    data.append(duplicated_value)
    # 写入文件
    with open('input.txt', 'w') as fd:
        fd.writelines(('%d\n' % num) for num in data)

    # 进行搜索
    result = search_duplicated('input.txt', 0, 9999, 8)

    assert result == duplicated_value
