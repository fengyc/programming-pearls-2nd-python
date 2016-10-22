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
import random
import os

MAX = int(1e7)  #所有数字均不超过 MAX


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


def merge(input_files, output_file):
    """ 归并多个有序小文件到一个大文件

    :param input_files: 输入的有序小文件
    :param output_file: 输出的大文件
    :return:
    """
    fd_head_map = {}  # 每个文件的描述符号和文件当前整数
    # 打开输入的中间文件
    for f in input_files:
        fd = open(f, 'r')
        head = fd.readline()
        if not head:
            fd.close()
        else:
            fd_head_map[fd] = int(head.strip())
    # 打开输出文件
    fd_out = open(output_file, 'w')

    # 使用选择最小值输出
    while len(fd_head_map):
        min = MAX
        selected_fd = None
        for fd in fd_head_map.keys():
            if min > fd_head_map[fd]:
                min = fd_head_map[fd]
                selected_fd = fd
        # 被选择的文件读取下一个整数，已到文件结束则关闭
        next_head = selected_fd.readline()
        if not next_head:
            fd_head_map.pop(selected_fd)
            selected_fd.close()
        else:
            fd_head_map[selected_fd] = int(next_head)
        # 当前最小值输出
        fd_out.write('%07d\n' % min)

    # 本次合并完成
    fd_out.close()


def check(file):
    """ 检查文件是否已按小到大排序

    :param file: 待检查文件
    :return: 是否已排序
    """
    with open(file, 'r') as fd:
        # 第一个整数
        line = fd.readline()
        if not line:
            return True
        prev = int(line.strip())
        # 后续整数
        while True:
            line = fd.readline()
            if not line:
                return True
            else:
                num = int(line.strip())
                if num < prev:
                    return False


if __name__ == '__main__':
    input_file = 'input.txt'
    output_file = 'output.txt'

    # 生成输入文件，只生成 1M 个
    print('Generating')
    with open(input_file, 'w') as fd:
        for i in range(1024*1024):
            num = random.randint(0, MAX)
            fd.write('%07d\n' % num)

    # 进行分割，分为8个文件，每个文件 128K 个
    print('Splitting')
    temp_files = split(input_file, 1024*128)

    # 进行合并
    print('Merging')
    merge(temp_files, output_file)

    # 删除中间文件
    for f in temp_files:
        os.remove(f)

    # 检查
    print('Checking')
    if check(output_file):
        print("Success")
    else:
        print("Fail")
