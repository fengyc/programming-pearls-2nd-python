# -*- coding:utf-8 -*-
#
# 测试

import pytest
import random
import os

MAX = int(1e7)


def generate_input_file(input_file):
    """ 生成输入文件 """

    # 只生成 1M 个
    print('Generating')
    with open(input_file, 'w') as fd:
        for i in range(1024):
            cache = []
            for j in range(1024):
                cache.append(random.randint(0, MAX))
            s = '\n'.join(('%07d' % num for num in cache))
            fd.write(s+'\n')


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


@pytest.fixture(scope='module')
def input_file():
    file_name = 'input.txt'
    if not os.path.isfile(file_name):
        generate_input_file(file_name)
    return file_name


def test_merge_sort_1(input_file):
    from .a1_3_file_merge_sort_1 import split, merge

    temp_files = []
    try:
        print('Testing ch01 -> merge sort 1')
        print('Splitting')
        temp_files = split(input_file, 1024*1024//4)
        print('Merging')
        merge(temp_files, 'output.txt')
        print('Checking')
        result = check('output.txt')
        assert result
    finally:
        for temp_file in temp_files:
            os.remove(temp_file)


def test_merge_sort_2(input_file):
    from .a1_3_file_merge_sort_2 import split, merge

    temp_files = []
    try:
        print('Testing ch01 -> merge sort 2')
        print('Splitting')
        temp_files = split(input_file, 1024*1024//4)
        print('Merging')
        merge(temp_files, 'output.txt')
        print('Checking')
        result = check('output.txt')
        assert result
    finally:
        for temp_file in temp_files:
            os.remove(temp_file)


def test_multi_select_sort(input_file):
    from .a1_3_file_multi_select_sort import sort

    print('Testing ch01 -> multi select sort')
    print('Sorting')
    sort(input_file, 'output.txt', 1024*1024//4)
    print('Checking')
    result = check('output.txt')
    assert result


def test_bit_vector(input_file):
    from .a1_4_file_bit_vector import bit_sort

    print('Testing ch01 -> bit vector')
    print('Sorting')
    bit_sort(input_file, 'output.txt')
    print('Checking')
    result = check('output.txt')
    assert result


def test_simple_sort(input_file):
    from .a1_6_1_sort import sort

    print('Testing ch01 -> simple sort')
    print('Sorting')
    sort(input_file, 'output.txt')
    print('Checking')
    assert check('output.txt')
