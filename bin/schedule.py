#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# @Time    : 2020/12/29 上午1:47
# @Author  : TNanko
# @Site    : https://tnanko.github.io
# @File    : schedule.py
# @Software: PyCharm
import sys
import os
cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
sys.path.append(root_path)
import json
from crontab import CronTab
from setup import BASE_DIR
from utils.configuration import read


def pretty_dict(dict):
    """
    格式化输出 json 或者 dict 格式的变量
    :param dict:
    :return:
    """
    print(json.dumps(dict, indent=4, ensure_ascii=False))


def create_cron(skip_check_version=False):
    """
    添加定时任务
    :param skip_check_version:
    :return:
    """
    cron = CronTab(user=True)
    _, config_current = read(skip_check_version=skip_check_version)  # 读取所有配置
    jobs = config_current['jobs']  # 得到当前所有任务
    multi_script_jobs = []  # 多脚本任务

    # 读取每个 job 的 cron 表达式
    for key, value in jobs.items():
        try:
            scripts_path = f"{BASE_DIR}/{'scripts'}/{value['scripts_filename']}"  # 脚本绝对路径
            job = cron.new(command='python3 %s' % scripts_path, comment='TNanko Scripts')  # 创建一个c cron 任务
            job.setall(value['schedule']['cron'])  # 设置脚本运行频率
            if job.is_valid:
                continue
            else:
                print(f"定时任务 {key} 设置错误，请仔细检查 cron 表达式和对应的配置信息！")
            # print(job.is_enabled())
            # job.enable(enabled=False)
        except:
            multi_script_jobs.append(key)  # 单任务多脚本暂时没写
    cron.write()


def delete_cron():
    cron = CronTab(user=True)
    try:
        cron.remove_all(comment='TNanko Scripts')
        cron.write()
    except:
        print('未知错误，请联系作者')


def main():
    # delete_cron()
    # create_cron()
    pass


if __name__ == '__main__':
    main()