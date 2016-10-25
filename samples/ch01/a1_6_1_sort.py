# -*- coding:utf-8 -*-
#
# 简单的内置 sort
#


def sort(input_file, output_file):
    """ 使用内置 sort 进行原地排序

    :param input_file: 输入文件
    :param output_file: 输出文件
    :return:
    """
    chunk = []
    with open(input_file, 'r') as input_fd:
        line = input_fd.readline()
        while line:
            chunk.append(int(line.strip()))
            line = input_fd.readline()
        chunk.sort()
    with open(output_file, 'w') as output_fd:
        output_fd.writelines(('%07d\n' % num for num in chunk))
