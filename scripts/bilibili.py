#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# @Time    : 2020/12/5 下午9:13
# @Author  : TNanko
# @Site    : https://tnanko.github.io
# @File    : bilibili.py
# @Software: PyCharm
import sys
import os
cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
sys.path.append(root_path)
import json
import time
import requests
import traceback
from setup import get_standard_time, BASE_DIR
from utils import notify, log
from utils.configuration import read


def pretty_dict(dict):
    """
    格式化输出 json 或者 dict 格式的变量
    :param dict:
    :return:
    """
    return print(json.dumps(dict, indent=4, ensure_ascii=False))


def sign(headers):
    url = 'https://api.live.bilibili.com/sign/doSign'
    try:
        response = requests.get(url=url, headers=headers).json()
        # pretty_dict(response)
        if response['code'] == 0:
            return response['data']
        elif response['code'] == 1011040:
            return get_sign_info(headers=headers)
        else:
            return
    except:
        print(traceback.format_exc())
        return


def get_sign_info(headers):
    url = 'https://api.live.bilibili.com/sign/GetSignInfo'
    try:
        response = requests.get(url=url, headers=headers).json()
        # pretty_dict(response)
        if response['code'] == 0:
            return response['data']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def bilibili():
    # 读取 bilibili 配置
    config_latest, config_current = read()
    try:
        bilibili_config = config_current['jobs']['bilibili']
    except:
        print('配置文件中没有此任务！请更新您的配置文件')
        return
    # 脚本版本检测
    try:
        if bilibili_config['skip_check_script_version']:
            print('脚本配置参数 skip_check_script_version = true ，跳过脚本版本检测...')
        elif config_latest:
            if config_latest['jobs']['bilibili']['version'] > bilibili_config['version']:
                print(
                    f"检测到最新的脚本版本号为{config_latest['jobs']['bilibili']['version']}，当前脚本版本号：{bilibili_config['version']}")
            else:
                print('当前脚本为最新版本')
        else:
            print('未获取到最新脚本的版本号')
    except:
        print('程序运行异常，跳过脚本版本检测...')
    # 脚本名字
    scripts_filename = bilibili_config['scripts_filename']
    # 日志相关参数
    log_parameters = bilibili_config['log']

    if bilibili_config['enable']:
        # 获取config.yml账号信息
        accounts = bilibili_config['parameters']['ACCOUNTS']
        for account in accounts:
            headers = {
                'Cookie': account['COOKIE'],
                'Host': 'api.live.bilibili.com',
                'Origin': 'api.live.bilibili.com',
                'Referer': 'http://live.bilibili.com/',
                'Accept': 'application/json, text/javascript, */*; q=0.01',
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.4 Safari/605.1.15'
            }
            utc_datetime, beijing_datetime = get_standard_time()
            start_time = time.time()

            title = f'☆【bilibili】{beijing_datetime.strftime("%Y-%m-%d %H:%M:%S")} ☆'
            account_title = f"\n{'=' * 16}【bilibili】{utc_datetime.strftime('%Y-%m-%d %H:%M:%S')}/{beijing_datetime.strftime('%Y-%m-%d %H:%M:%S')} {'=' * 16}\n{title}"
            content = ''
            sign_result = sign(headers=headers)
            if sign_result:
                content += f"【bilibili】签到成功！本月累计({sign_result['hadSignDays']},{sign_result['allDays']})次，说明{sign_result['text']}"
            else:
                content += f"【bilibili】签到失败！说明：{sign_result['message']}"

            content += f'\n🕛耗时：%.2f秒' % (time.time() - start_time)
            content += f'\n如果帮助到您可以点下🌟STAR鼓励我一下，谢谢~'

            if log_parameters['enable']:
                try:
                    # folder_path = os.path.join(BASE_DIR, 'log')  # 可能 windows 系统不适用（未测试）
                    folder_path = BASE_DIR + f'/log/{scripts_filename[:-3]}'
                    if not os.path.isdir(folder_path):
                        print('对应的日志文件夹不存在，创建日志文件夹...')
                        os.makedirs(folder_path)
                    beijing_datetime.strftime("%Y-%m-%d %H:%M:%S")
                    log_path = folder_path + '/%s.log' % beijing_datetime.strftime('%Y-%m-%d')
                    # 写入日志
                    log.write_scripts_log(path=log_path, msg='%s\n\n%s' % (account_title, content))
                    # 删除过期日志
                    log.delete_scripts_log(path=folder_path, valid_period=log_parameters['valid_period'])
                except:
                    print('写入日志失败！%s\n%s' % (account_title, content))
            else:
                print(account_title + content)

            if bilibili_config['notify']:
                # 消息推送方式
                notify_mode = bilibili_config['notify_mode']
                try:
                    # 推送消息
                    notify.send(title=title, content=content, notify_mode=notify_mode)
                except:
                    print('请确保配置文件的对应的脚本任务中，参数 notify_mode 下面有推送方式\n')
            else:
                print('未进行消息推送。如需发送消息推送，请确保配置文件的对应的脚本任务中，参数 notify 的值为 true\n')
    else:
        print('未执行该任务，如需执行请在配置文件的对应的任务中，将参数 enable 设置为 true\n')


def main():
    bilibili()


if __name__ == '__main__':
    main()
