#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# @Time    : 2020/11/30 1:13
# @Author  : TNanko
# @Site    : https://tnanko.github.io
# @File    : configuration.py
# @Software: PyCharm
import sys
import os
cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
sys.path.append(root_path)
import yaml
from setup import BASE_DIR


def read():
    """
    支持 github action 和本地文件读取（github action 未测试）
    :return: 返回配置信息
    """
    if 'CONFIG' in os.environ:
        config = yaml.load(os.environ['CONFIG'], Loader=yaml.FullLoader)
        return config
    else:
        path = BASE_DIR + '/config/config.yml'
        with open(path, mode='r', encoding='utf-8') as obj:
            config = yaml.load(obj, Loader=yaml.FullLoader)  # <class 'dict'>
            return config


if __name__ == '__main__':
    print(read())
