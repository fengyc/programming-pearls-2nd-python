# -*- coding: utf-8 -*-
#
# 问题:
# 数字保存在文件中，每个数字一行，每个数字均为7位
#
# 一次读取后分割为多个中间工作文件，用多路归并排序，通过败者树进行优化减少比较
#
# 基本思路:
# 1. 从输入读取可用内存大小的数据，对数据进行内部排序，保存到中间文件
# 2. 每次同时打开 K 个中间文件，归并输出到一个更大的中间文件
# 3. 将更大的中间文件重复步骤2，直到得到唯一结果文件
# 4. 使用 uuid 生成中间文件名，也可用 tempfile 处理中间文件
#
# 注意:
# 1. 败者树是一棵完全二叉树，可使用列表保存，这里分开叶子节点和比较节点存储
# 2. 未处理文件异常等
# 3. 未有处理重复数据，重复数据不影响排序和输出

import uuid
import random
import os

MAX = int(1e7)  #所有数字均不超过 MAX


def create_tree(leaves):
    """ 创建败者树

    :param leaves: 叶子节点
    :return: 败者树(不包含叶子节点)
    """
    tree = []
    n = len(leaves)
    # 清空败者树，设置指向的叶子节点为 -1
    for i in range(n):
        tree.append(-1)
    # 从后往前调整
    for i in range(n-1, -1, -1):
        adjust_tree(tree, leaves, i)
    return tree


def adjust_tree(tree, leaves, s):
    """ 因叶子节点 s 改变调整败者树

    :param tree: 败者树
    :param leaves: 叶子节点
    :param s: 改变的叶子节点下标
    :return:
    """
    # 首先根据叶子节点下标计算出对应的败者树中父节点下标
    parent = (s + len(tree)) // 2
    while parent > 0:
        if s == -1:
            break
        # 如果败者树中 parent 位置不指向叶子节点的位置
        # 或者 parent 位置的叶子节点被打败(以大为败)，那么需要调整
        if tree[parent] == -1 or leaves[s]['num'] > leaves[tree[parent]]['num']:
            tmp = s
            s = tree[parent]    # s 指向胜者
            tree[parent] = tmp  # 败者保存到 parent 位置
        # 向上调整
        parent //= 2
    # 冠军节点
    tree[0] = s


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
    """ 使用败者树归并多个有序小文件到一个大文件

    :param input_files: 输入的有序小文件
    :param output_file: 输出的大文件
    :return:
    """
    # 初始化
    fd_heads = []  # 每个文件的描述符号和文件当前整数
    # 打开输入的中间文件
    for f in input_files:
        fd = open(f, 'r')
        line = fd.readline()
        if not line:
            num = MAX
            fd.close()
        else:
            num = int(line.strip())
        fd_heads.append({
            'fd': fd,
            'num': num
        })
    # 创建败者树
    tree = create_tree(fd_heads)

    # 从败者树取冠军节点
    with open(output_file, 'w') as fd_out:
        # 循环取最小值， 当冠军节点不是 MAX 时进行循环读取调整
        while fd_heads[tree[0]]['num'] < MAX:
            champion = fd_heads[tree[0]]
            fd_out.write('%07d\n' % champion['num'])
            # 冠军节点更新
            line = champion['fd'].readline()
            if not line:
                champion['num'] = MAX
                champion['fd'].close()
            else:
                champion['num'] = int(line.strip())
            # 调整败者树
            adjust_tree(tree, fd_heads, tree[0])


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
        for i in range(1024):
            num = random.randint(0, MAX)
            fd.write('%07d\n' % num)

    # 进行分割，分为8个文件，每个文件 128K 个
    print('Splitting')
    temp_files = split(input_file, 128)

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
