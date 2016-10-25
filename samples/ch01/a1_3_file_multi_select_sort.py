# -*- coding:utf-8 -*-
#
# 问题:
# 数字保存在文件中，每个数字一行，每个数字均为7位
#
# 多次读取输入文件，并选择排序，每次选择的范围为 [n*chunk_size， (n+1)*chunk_size)
# 然后进行内部排序
#
# 基本思路:
# 1. 每次从文件读取范围为 n*chunk_size ~ (n+1)*chunk_size 的数字
# 2. 对数据进行内部排序，输出到输出文件
# 3. 重复多次直到输入文件读取完毕
#
# 注意:
# 1. 未处理文件异常等
# 2. 未有处理重复数据，重复数据不影响排序和输出
# 3. 内部的排序可直接使用字符串(需要更多空间)，或者是转换为数字(需要字符串数字的转换时间)

from . import MAX


def sort(input_file, output_file, chunk_size):
    """ 多次范围选择文件排序

    :param input_file: 输入文件
    :param output_file: 输出文件
    :param chunk_size: 每次选择的范围增量
    :return:
    """
    with open(input_file, 'r') as input_fd, \
            open(output_file, 'w') as output_file:
        chunk = []
        chunk_min = 0
        chunk_max = chunk_min + chunk_size
        while True:
            line = input_fd.readline()
            # 本次读取输入文件结束，进行输出
            if not line:
                # 输出数据
                if chunk:
                    chunk.sort()
                    for num in chunk:
                        output_file.write('%07d\n' % num)
                    del chunk
                # 更新下次需要读取的范围，并判断是否已超过范围
                chunk_min = chunk_max
                chunk_max = chunk_min + chunk_size
                if chunk_min >= MAX:
                    return
                # 重置 fd 游标
                input_fd.seek(0, 0)
                chunk = []
            else:
                # 判断数据是否在本次读取范围内
                num = int(line.strip())
                if chunk_min <= num < chunk_max:
                    chunk.append(num)
