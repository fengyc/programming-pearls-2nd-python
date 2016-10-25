# -*- coding:utf-8 -*-
#
# 问题:
# 数字保存在文件中，每个数字一行，每个数字均为7位
#
# 利用位图的方式进行数据排序，并且隐含有去重的功能
#
# 基本思路:
# 1. 每个数字对应大数的一个位，若数字出现则该位置1
# 2. 是对数据进行压缩了，一个32位的整数，变成了一个位
# 3. 数据范围为 [0，MAX) 时，需要的内存字节数为 MAX / 8 ， 1e7 约为 1.22 M
#
# 注意:
# 1. 重复数据会被去重
# 2. 使用 c/c++ 操作会更好

import ctypes
import math
from . import MAX

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
