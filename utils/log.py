#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# @Time    : 2021/1/2 下午2:48
# @Author  : TNanko
# @Site    : https://tnanko.github.io
# @File    : log.py
# @Software: PyCharm
import sys
import os
cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
sys.path.append(root_path)
import logging
from setup import BASE_DIR

def write_scripts_log(path, msg):
    """
    写日志
    :param path: 日志文件目录
    :param msg: 写入的内容
    :return:
    """
    logger = logging.getLogger("TNanko's Scripts")
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        # 创建 handler
        fh = logging.FileHandler(path, encoding='utf-8')
        ch = logging.StreamHandler()

        # 设置输出日志格式
        formatter = logging.Formatter(
            fmt='%(asctime)s %(name)s %(levelname)s %(message)s\n\n',
            datefmt='%Y-%m-%d  %H:%M:%S %a'
        )

        # 为 handler 指定输出格式
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)

        # 为 logger 添加的日志处理器
        logger.addHandler(fh)
        logger.addHandler(ch)
    logger.info(msg=msg)

def delete_scripts_log(path, valid_period):
    """
    删除日志
    :param path: 日志所在的文件夹
    :param valid_period: 保存日志的天数
    :return:
    """
    if os.path.isdir(path):
        files = os.listdir(path)
        files.sort(reverse=True)
        for i in files[valid_period:]:
            # print(path + '/%s' % i)
            os.remove(path + '/%s' % i)
    else:
        print('参数 path 错误：非文件夹路径')

def main():
    # path = BASE_DIR + '/log/test.log'
    # write_scripts_log(path=path, msg='test')
    print(BASE_DIR)
    # delete_scripts_log('/Scripts/log/qq_read', 3)

if __name__ == '__main__':
    main()