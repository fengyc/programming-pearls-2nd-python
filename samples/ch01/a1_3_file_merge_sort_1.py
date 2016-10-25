# -*- coding: utf-8 -*-
#
# 问题:
# 数字保存在文件中，每个数字一行，每个数字均为7位
#
# 一次读取后分割为多个中间工作文件，用多路归并排序
#
# 基本思路:
# 1. 从输入读取可用内存大小的数据，对数据进行内部排序,保存到中间文件
# 2. 每次同时打开 K 个中间文件,归并输出到一个更大的中间文件
# 3. 将更大的中间文件重复步骤2，直到得到唯一结果文件
# 4. 使用 uuid 生成中间文件名，也可用 tempfile 处理中间文件
#
# 注意:
# 1. python 中的列表使用的内存包括数据结构开销，仅以 chunk_size 表示数据块大小
# 2. 未处理文件异常等
# 3. 未有处理重复数据，重复数据不影响排序和输出
# 4. 内部的排序可直接使用字符串(需要更多空间)，或者是转换为数字(需要字符串数字的转换时间)
#
# 优化:
# 使用败者树，减少归并时的比较次数，K越大加速越明显

import uuid
import math
from . import MAX


def split(input_file, chunk_size):
    """ 分割大文件为小文件，并且将小文件数据排序

    :param input_file: 输入文件
    :param chunk_size: 块大小
    :return: 小文件列表
    """
    temp_files = []
    chunk = []
    with open(input_file, 'r') as f:
        while True:
            line = f.readline()
            # 如果已结束或内存已满，则输出到临时文件
            if not line or len(chunk) >= chunk_size:
                if chunk:
                    chunk.sort()
                    temp_file = uuid.uuid4().hex
                    with open(temp_file, 'w') as temp_fd:
                        for num in chunk:
                            temp_fd.write(str(num)+'\n')
                    temp_files.append(temp_file)
                    del chunk
                    chunk = []
                if not line:
                    break
            num = int(line.strip())
            chunk.append(num)
    return temp_files


def merge(input_files, output_file, chunk_size):
    """ 归并多个有序小文件到一个大文件

    :param input_files: 输入的有序小文件
    :param output_file: 输出的大文件
    :param chunk_size: 块大小
    :return:
    """
    fd_head_map = {}  # 每个文件的描述符号和文件当前整数缓存和访问下标
    cache_size = math.floor(chunk_size / (len(input_files) + 1))
    # 打开输入的中间文件
    for f in input_files:
        fd = open(f, 'r')
        cache = []
        for i in range(cache_size):
            line = fd.readline()
            if not line:
                fd.close()
                break
            else:
                cache.append(int(line.strip()))
        if cache:
            fd_head_map[fd] = [cache, 0]
    # 打开输出文件
    fd_out = open(output_file, 'w')
    output_cache = []

    # 使用选择最小值输出
    while fd_head_map:
        min = MAX
        selected_fd = None
        for fd, head in fd_head_map.items():
            if min > head[0][head[1]]:
                min = head[0][head[1]]
                selected_fd = fd
        # 被选择的文件更新缓存，已到文件结束则关闭
        fd_head_map[selected_fd][1] += 1
        if fd_head_map[selected_fd][1] >= len(fd_head_map[selected_fd][0]):
            del fd_head_map[selected_fd]
            cache = []
            if not selected_fd.closed:
                for i in range(cache_size):
                    line = selected_fd.readline()
                    if not line:
                        selected_fd.close()
                        break
                    else:
                        cache.append(int(line.strip()))
            if cache:
                fd_head_map[selected_fd] = [cache, 0]

        # 当前最小值输出
        output_cache.append(min)
        if len(output_cache) >= cache_size or not len(fd_head_map):
            fd_out.writelines(('%07d\n' % num for num in output_cache))
            del output_cache
            output_cache = []

    # 本次合并完成，关闭输出
    fd_out.close()
