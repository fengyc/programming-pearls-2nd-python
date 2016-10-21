# -*- coding:utf-8 -*-
#
# 问题:
# 数字保存在文件中,每个数字一行,每个数字均为7位
#
# 利用位图的方式进行数据排序,并且隐含有去重的功能
#
# 基本思路:
# 1. 每个数字对应大数的一个位,若数字出现则该位置1
# 2. 是对数据进行压缩了,一个32位的整数,变成了一个位
# 3. 数据范围为 [0,MAX) 时,需要的内存字节数为 MAX / 8 , 1e7 约为 1.22 M
#
# 注意:
# 1. 重复数据会被去重
# 2. 使用 c/c++ 操作会更好

import random
import ctypes
import math

MAX = int(1e7)

BitVector = ctypes.c_ubyte * math.ceil(MAX / 8)


def set_bit(vector, offset):
    """ 置 1

    :param vector: 位图
    :param offset: 位偏移
    :return:
    """
    byte_index = offset >> 3
    bit_offset = offset & 7
    mask = 1 << bit_offset
    vector[byte_index] |= mask


def clear_bit(vector, offset):
    """ 清 0

    :param vector: 位图
    :param offset: 位偏移
    :return:
    """
    byte_index = offset >> 3
    bit_offset = offset & 7
    mask = ~(1 << bit_offset)
    vector[byte_index] &= mask


def get_bit(vector, offset):
    """ 取值

    :param vector: 位图
    :param offset: 位偏移
    :return: 对应的位是否为 1
    """
    byte_index = offset >> 3
    if vector[byte_index] == 0:
        return False
    bit_offset = offset & 7
    mask = 1 << bit_offset
    return vector[byte_index] & mask != 0


def bit_sort(input_file, output_file):
    vector = BitVector()
    ctypes.memset(vector, 0, len(vector))

    with open(input_file, 'r') as input_fd:
        while True:
            line = input_fd.readline()
            if not line:
                with open(output_file, 'w') as output_fd:
                    for i in range(MAX):
                        if get_bit(vector, i):
                            output_fd.write('%07d\n' % i)
                return
            else:
                num = int(line.strip())
                set_bit(vector, num)


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

    # 生成输入文件,只生成 1M 个
    print('Generating')
    with open(input_file, 'w') as fd:
        for i in range(1024*1024):
            num = random.randint(0, MAX)
            fd.write('%07d\n' % num)

    # 排序
    print('Sorting')
    bit_sort(input_file, output_file)

    # 检查
    print('Checking')
    if check(output_file):
        print('Success')
    else:
        print('Fail')