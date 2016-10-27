# -*- coding:utf-8 -*-
#
# 对顺序文件保存的矩阵进行转置
#
# 假设文件先按照行号，再按照列号的顺序保存每个数据。对每个数据使用行号和列号标识，输出到中间
# 文件；然后对中间文件进行排序，先比较列号再比较行号，输出到排序后的中间文件；处理排序后的中
# 间文件，删除行号和列号

import uuid
import os


def add_identifier(input_file, output_file, m=4000):
    """ 为文件加上标识，并输出到文件

    :param input_file: 输入文件
    :param output_file: 输出文件
    :param m: 列长度
    """
    with open(input_file, 'r') as input_fd,\
            open(output_file, 'w') as output_fd:
        a = b = 0   # 行号列号计数
        while True:
            line = input_fd.readline()
            if not line:
                break
            num = int(line.strip())
            output_fd.write('%d %d %d\n' % (a, b, num))
            b += 1  # 列号 +1
            if b >= m:
                b = 0
                a += 1


def remove_identifier(input_file, output_file):
    """ 移动文件中的标识，并输出到文件

    :param input_file: 输出文件
    :param output_file: 输出文件
    """
    with open(input_file, 'r') as input_fd, \
            open(output_file, 'w') as output_fd:
        while True:
            line = input_fd.readline()
            if not line:
                break
            num = int(line.split()[2])
            output_fd.write('%d\n' % num)


def compare(a, b):
    """ 比较两个带标识的数据记录 """
    m = (int(i) for i in a.split())
    n = (int(i) for i in b.split())
    return m <= n


def tape_sort(input_file, output_file, compare):
    """ 磁带排序 """
    pass


def transpose(input_file, output_file):
    """ 转置

    :param input_file: 输入文件
    :param output_file: 输出文件
    """
    temp_file1 = uuid.uuid4().hex
    add_identifier(input_file, temp_file1)
    # 磁带排序
    temp_file2 = uuid.uuid4().hex
    tape_sort(temp_file1, temp_file2, compare)
    # 移除标识
    remove_identifier(temp_file2, output_file)
    # 清理
    os.remove(temp_file2)
    os.remove(temp_file1)
