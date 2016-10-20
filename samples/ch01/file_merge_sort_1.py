# -*- coding: utf-8 -*-
#
# 一次读取后分割为多个中间工作文件,用多路归并排序
#
# 问题:
# 数字保存在文件中,每个数字一行
#
# 基本思路:
# 1. 从输入读取可用内存大小的数据,对数据进行内部排序,保存到中间文件
# 2. 每次同时打开 K 个中间文件,归并输出到一个更大的中间文件
# 3. 将更大的中间文件重复步骤2,直到得到唯一结果文件
#
# 优化:
# 使用败者树,减少归并时的比较次数,K越大加速越明显

import uuid


MEM_SIZE = 1024*1024
K = 80
INPUT_FILE = 'input.txt'
OUTPUT_FILE = 'output.txt'
TEMP_FILES = []


def split(input_file, chunk_size):
    """ 分割大文件为小文件

    :param input_file: 输入文件
    :param chunk_size: 块大小
    :return: 小文件列表
    """
    temp_files = []
    with open(input_file, 'r') as f:
        end = False
        while not end:
            chunk = []
            for i in range(chunk_size):
                num = f.readline()
                if not num:
                    # end of file
                    end = True
                    break
                chunk.append(int(num))
            if chunk:
                chunk.sort()
                temp_file = uuid.uuid4().hex
                temp_files.append(temp_file)
                with open(temp_file, 'w') as tf:
                    for n in chunk:
                        tf.write(str(n)+'\n')
    return temp_files


def merge(input_files, output_file):
    for f in input_files:



