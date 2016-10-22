# -*- coding:utf-8 -*-
#
# 测试

import random

MAX = int(1e7)


def generate_input_file(input_file):
    """ 生成输入文件 """

    # 只生成 1M 个
    print('Generating')
    with open(input_file, 'w') as fd:
        for i in range(1024 * 1024):
            num = random.randint(0, MAX)
            fd.write('%07d\n' % num)


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


def test_merge_sort_1():
    from .a1_3_file_merge_sort_1 import split, merge

