#!/usr/bin/env python3
# _*_ coding:utf-8 _*_

# @Time    : 2020/12/3 1:28
# @Author  : TNanko
# @Site    : https://tnanko.github.io
# @File    : qq_read.py
# @Software: PyCharm
"""
此脚本使用 Python 语言根据 https://github.com/ziye12/JavaScript/blob/master/qqread.js 改写
需要自行使用代理软件获取 书籍 url 和 cookie
1. MitM 添加 hostname=mqqapi.reader.qq.com
2. 添加改写
    quanx
    https:\/\/mqqapi\.reader\.qq\.com\/mqq\/addReadTimeWithBid? url script-request-header https://raw.githubusercontent.com/ziye12/JavaScript/master/qqread.js

    loon
    http-request https:\/\/mqqapi\.reader\.qq\.com\/mqq\/addReadTimeWithBid? script-path=https://raw.githubusercontent.com/ziye12/JavaScript/master/qqread.js, requires-header=true, tag=企鹅读书获取cookie

    surge
    企鹅读书获取cookie = type=http-request,pattern=https:\/\/mqqapi\.reader\.qq\.com\/mqq\/addReadTimeWithBid?,script-path=https://raw.githubusercontent.com/ziye12/JavaScript/master/qqread.js, requires-header=true
3. 打开企鹅读书，随便浏览一本数几秒后退出，获取书籍 url 和 headers
4. 根据抓到的 headers 将 ywsession 和 Cookie 分别填写到配置文件中 YWSESSION 和 COOKIE （不要带引号，注意冒号后面的空格）
"""

import sys
import os
cur_path = os.path.abspath(os.path.dirname(__file__))
root_path = os.path.split(cur_path)[0]
sys.path.append(root_path)
import json
import re
import time
import requests
import traceback
from setup import get_standard_time
from utils import notify
from utils.configuration import read


def pretty_dict(dict):
    """
    格式化输出 json 或者 dict 格式的变量
    :param dict:
    :return:
    """
    return print(json.dumps(dict, indent=4, ensure_ascii=False))


def get_user_info(headers):
    """
    获取任务信息
    :param headers:
    :return:
    """
    url = 'https://mqqapi.reader.qq.com/mqq/user/init'
    try:
        response = requests.get(url=url, headers=headers).json()
        if response['code'] == 0:
            return response['data']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def get_daily_beans(headers):
    """
    阅豆签到
    :param headers:
    :return:
    """
    url = 'https://mqqapi.reader.qq.com/mqq/sign_in/user'
    try:
        response = requests.post(url=url, headers=headers).json()
        if response['code'] == 0:
            return response['data']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def get_daily_tasks(headers):
    """
    获取今日任务列表
    :param headers:
    :return:
    """
    url = 'https://mqqapi.reader.qq.com/mqq/red_packet/user/page?fromGuid='
    try:
        response = requests.get(url=url, headers=headers).json()
        if response['code'] == 0:
            # print('获取今日任务')
            # pretty_dict(response['data'])
            return response['data']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def get_today_read_time(headers):
    """
    得到今日阅读时长
    :param headers:
    :return:
    """
    url = 'https://mqqapi.reader.qq.com/mqq/page/config?router=%2Fpages%2Fbook-read%2Findex&options='
    try:
        response = requests.get(url=url, headers=headers).json()
        # print('今日阅读')
        # pretty_dict(response)
        if response['code'] == 0:
            return response['data']['pageParams']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def read_time_reward_tasks(headers, seconds):
    """
    阅读奖励，好像一个号只能领一次
    :param headers:
    :param seconds:
    :return:
    """
    url = f'https://mqqapi.reader.qq.com/mqq/red_packet/user/read_time_reward?seconds={seconds}'
    try:
        response = requests.get(url=url, headers=headers).json()
        print('阅读奖励')
        pretty_dict(response)
        if response['code'] == 0:
            return response['data']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def get_week_read_time(headers):
    """
    周阅读时长
    :param headers:
    :return:
    """
    url = 'https://mqqapi.reader.qq.com/mqq/v1/bookShelfInit'
    try:
        response = requests.get(url=url, headers=headers).json()
        # print('周阅读时长')
        # pretty_dict(response)
        if response['code'] == 0:
            return response['data']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def read_now(headers):
    """
    立即阅读
    :param headers:
    :return:
    """
    url = 'https://mqqapi.reader.qq.com/mqq/red_packet/user/read_book'
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


def read_tasks(headers, seconds):
    """
    每日阅读任务
    :param headers:
    :param seconds:
    :return:
    """
    url = f'https://mqqapi.reader.qq.com/mqq/red_packet/user/read_time?seconds={seconds}'
    try:
        response = requests.get(url=url, headers=headers).json()
        if response['code'] == 0:
            return response['data']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def daily_sign(headers):
    """
    今日打卡
    :param headers:
    :return:
    """
    url = 'https://mqqapi.reader.qq.com/mqq/red_packet/user/clock_in/page'
    try:
        response = requests.get(url=url, headers=headers).json()
        if response['code'] == 0:
            return response['data']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def watch_daily_sign_ads(headers):
    """
    今日打卡看广告翻倍
    :param headers:
    :return:
    """
    url = 'https://mqqapi.reader.qq.com/mqq/red_packet/user/clock_in_video'
    try:
        response = requests.get(url=url, headers=headers).json()
        time.sleep(3)
        if response['code'] == 0:
            return response['data']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def watch_videos(headers):
    """
    看视频，拿金币
    :param headers:
    :return:
    """
    url = 'https://mqqapi.reader.qq.com/mqq/red_packet/user/watch_video'
    try:
        response = requests.get(url=url, headers=headers).json()
        if response['code'] == 0:
            return response['data']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def open_treasure_box(headers):
    """
    每20分钟开一次宝箱
    :param headers:
    :return:
    """
    url = 'https://mqqapi.reader.qq.com/mqq/red_packet/user/treasure_box'
    try:
        response = requests.get(url=url, headers=headers).json()
        time.sleep(15)
        if response['code'] == 0:
            return response['data']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def watch_treasure_box_ads(headers):
    """
    看广告，宝箱奖励翻倍
    :param headers:
    :return:
    """
    url = 'https://mqqapi.reader.qq.com/mqq/red_packet/user/treasure_box_video'
    try:
        response = requests.get(url=url, headers=headers).json()
        time.sleep(15)
        if response['code'] == 0:
            return response['data']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def get_week_read_tasks(headers):
    """
    周阅读奖励查询
    :param headers:
    :return:
    """
    url = 'https://mqqapi.reader.qq.com/mqq/pickPackageInit'
    try:
        response = requests.get(url=url, headers=headers).json()
        if response['code'] == 0:
            return response['data']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def get_week_read_reward(headers, read_time):
    """
    领取周阅读奖励
    :param headers:
    :param read_time: 阅读时长
    :return:
    """
    url = f'https://mqqapi.reader.qq.com/mqq/pickPackage?readTime={read_time}'
    try:
        response = requests.get(url=url, headers=headers).json()
        # print(f'领取周阅读奖励({read_time})')
        # pretty_dict(response)
        if response['code'] == 0:
            return response['data']
        else:
            return
    except:
        print(traceback.format_exc())
        return


def read_books(headers, book_url, upload_time):
    """
    刷时长
    :param headers:
    :return:
    """
    findtime = re.compile(r'readTime=(.*?)&read_')
    url = re.sub(findtime.findall(book_url)[0], str(upload_time * 60 * 1000), str(book_url))
    # url = book_url.replace('readTime=', 'readTime=' + str(upload_time))
    try:
        response = requests.get(url=url, headers=headers).json()
        if response['code'] == 0:
            return True
        else:
            return
    except:
        print(traceback.format_exc())
        return


def qq_read():
    try:
        # 读取企鹅阅读配置
        qq_read_config = read()['jobs']['qq_read']
    except:
        print('配置文件中没有此任务！请更新您的配置文件')
        return
    # 获取config.yml账号信息
    accounts = qq_read_config['parameters']['ACCOUNTS']
    # 每次上传的时间
    upload_time = qq_read_config['parameters']['UPLOAD_TIME']
    # 每天最大阅读时长
    max_read_time = qq_read_config['parameters']['MAX_READ_TIME']
    # 消息推送方式
    notify_mode = qq_read_config['notify_mode']

    utc_datetime, beijing_datetime = get_standard_time()
    if beijing_datetime.hour == 0 and beijing_datetime.minute <= 10:
        notify.send(title=f'☆【企鹅阅读】{beijing_datetime.strftime("%Y-%m-%d %H:%M:%S")} ☆',
                    content='请去QQ企鹅读书小程序中手动开一次宝箱或者看视频！', notify_mode=notify_mode)

    # 开启脚本执行
    if qq_read_config['enable']:
        for account in accounts:
            book_url = account['BOOK_URL']
            headers = {
                'Accept': '*/*',
                'ywsession': account['YWSESSION'],
                'Connection': 'keep-alive',
                'Content-Type': 'application/json',
                'Cookie': account['COOKIE'],
                'Host': 'mqqapi.reader.qq.com',
                'User-Agent': 'QQ/8.4.17.638 CFNetwork/1197 Darwin/20.0.0',
                'Referer': 'https://appservice.qq.com/1110657249/0.30.0/page-frame.html',
                'Accept-Language': 'zh-cn',
                'Accept-Encoding': 'gzip, deflate, br',
                'mpversion': '0.30.0'
            }
            symbol = '=' * 16
            print(
                f'\n{symbol}【企鹅阅读】{utc_datetime.strftime("%Y-%m-%d %H:%M:%S")}/{beijing_datetime.strftime("%Y-%m-%d %H:%M:%S")} {symbol}\n')

            start_time = time.time()
            title = f'☆【企鹅阅读】{beijing_datetime.strftime("%Y-%m-%d %H:%M:%S")} ☆'
            content = ''

            # 获取用户信息（昵称）
            user_info = get_user_info(headers=headers)
            if user_info:
                content += f'【用户昵称】{user_info["user"]["nickName"]}'
            # 获取任务列表，查询金币余额
            daily_tasks = get_daily_tasks(headers=headers)
            if daily_tasks:
                content += f'\n【金币余额】剩余{daily_tasks["user"]["amount"]}金币，可提现{daily_tasks["user"]["amount"] // 10000}元'
            # 查询本周阅读时长
            week_read_time = get_week_read_time(headers=headers)
            if week_read_time:
                content += f'\n【本周阅读】{week_read_time["readTime"] // 60}小时{week_read_time["readTime"] % 60}分钟'
            # 查询今日阅读时长
            today_read_time = get_today_read_time(headers=headers)
            if today_read_time:
                content += f'\n【今日阅读】{today_read_time["todayReadSeconds"] // 3600}小时{today_read_time["todayReadSeconds"] // 60 % 60}分钟'
            # 输出任务列表中的信息
            if daily_tasks:
                content += f'\n【{daily_tasks["taskList"][0]["title"]}】{daily_tasks["taskList"][0]["amount"]}金币，{daily_tasks["taskList"][0]["actionText"]}'
                content += f'\n【{daily_tasks["taskList"][1]["title"]}】{daily_tasks["taskList"][1]["amount"]}金币，{daily_tasks["taskList"][1]["actionText"]}'
                content += f'\n【{daily_tasks["taskList"][2]["title"]}】{daily_tasks["taskList"][2]["amount"]}金币，{daily_tasks["taskList"][2]["actionText"]}'
                content += f'\n【{daily_tasks["taskList"][3]["title"]}】{daily_tasks["taskList"][3]["amount"]}金币，{daily_tasks["taskList"][3]["actionText"]}{daily_tasks["taskList"][3]["subTitle"]}'
                content += f'\n【邀请任务】{daily_tasks["invite"]["month"]}月第{daily_tasks["invite"]["issue"]}期({daily_tasks["invite"]["dayRange"]})，已邀{daily_tasks["invite"]["inviteCount"]}人，再邀请{daily_tasks["invite"]["nextInviteConfig"]["count"]}人可获{daily_tasks["invite"]["nextInviteConfig"]["amount"]}金币'
                content += f'\n【粉丝分成】已有{daily_tasks["fans"]["fansCount"]}个粉丝，今日获得分成{daily_tasks["fans"]["todayAmount"]}金币'
                content += f'\n【宝箱任务】已开{daily_tasks["treasureBox"]["count"]}个宝箱，下一个宝箱{daily_tasks["treasureBox"]["tipText"]}'

            # 每日签到
            daily_beans = get_daily_beans(headers=headers)
            if daily_beans and daily_beans['takeTicket'] > 0:
                content += f"\n【阅豆签到】获得{daily_beans['takeTicket']}阅豆"

            # 阅读奖励，好像每个账号只能领一次
            if not today_read_time['readTimeRewardTask'][len(today_read_time['readTimeRewardTask']) - 1]['doneFlag']:
                seconds = [60, 180, 360, 600, 900, 1200, 1500]
                for i in seconds:
                    read_time_reward = read_time_reward_tasks(headers=headers, seconds=i)
                    if read_time_reward:
                        content += f"\n【阅读奖励】阅读{i}秒，获得金币{read_time_reward['amount']}"

            # 立即阅读《xxx》
            if daily_tasks['taskList'][0]['enableFlag']:
                read_now_reward = read_now(headers=headers)
                if read_now_reward:
                    content += f'\n【{daily_tasks["taskList"][0]["title"]}】获得{read_now_reward["amount"]}金币'

            # 阅读任务
            if daily_tasks['taskList'][1]['enableFlag']:
                for task in daily_tasks['taskList'][1]['config']:
                    if task['enableFlag'] and not task['doneFlag']:
                        read_reward = read_tasks(headers=headers, seconds=task['seconds'])
                        if read_reward and read_reward['amount'] > 0:
                            content += f"\n【阅读任务】阅读{task['timeStr']}，获得{read_reward['amount']}金币"

            # 今日打卡
            if daily_tasks['taskList'][2]['enableFlag']:
                sign_reward = daily_sign(headers=headers)
                if sign_reward:
                    content += f"\n【{daily_tasks['taskList'][2]['title']}】获得{sign_reward['todayAmount']}金币，已连续签到{sign_reward['clockInDays']}天"
                # 打卡翻倍
                if sign_reward['videoDoneFlag'] == 0:
                    sign_ads_reward = watch_daily_sign_ads(headers=headers)
                    if sign_ads_reward:
                        content += f"\n【打卡翻倍】获得{sign_ads_reward['amount']}金币"

            # 看视频
            if daily_tasks['taskList'][3]['enableFlag']:
                finish_count = int(daily_tasks["taskList"][3]["subTitle"][1:2])
                total_count = int(daily_tasks["taskList"][3]["subTitle"][3:4])
                # for i in range(1, total_count+1):
                watch_videos_reward = watch_videos(headers=headers)
                if watch_videos_reward:
                    content += f"\n【视频奖励】获得{watch_videos_reward['amount']}金币({finish_count + 1}/{total_count})"

            # 周阅读时长奖励查询
            week_read_rewards = get_week_read_tasks(headers=headers)
            # 当周阅读时间 >= 最大奖励所需要的时间(1200分钟)，领取奖励
            if week_read_time['readTime'] >= week_read_rewards[len(week_read_rewards) - 1]['readTime']:
                for week_read_reward in week_read_rewards:
                    if not week_read_reward['isPick']:
                        reward = get_week_read_reward(headers=headers, read_time=week_read_reward['readTime'])
                        if reward:
                            content += f"\n【周时长奖励】领取{week_read_reward['readTime']}时长奖励成功"

            # 开宝箱领金币
            if daily_tasks['treasureBox']['doneFlag'] == 0:
                treasure_box_reward = open_treasure_box(headers=headers)
                if treasure_box_reward:
                    content += f"\n【开启第{treasure_box_reward['count']}个宝箱】获得{treasure_box_reward['amount']}金币"

            # 宝箱金币奖励翻倍
            daily_tasks = get_daily_tasks(headers=headers)
            if daily_tasks['treasureBox']['videoDoneFlag'] == 0:
                treasure_box_ads_reward = watch_treasure_box_ads(headers=headers)  # 这边有点问题
                if treasure_box_ads_reward:
                    content += f"\n【宝箱奖励翻倍】获得{treasure_box_ads_reward['amount']}金币"

            # 读书刷时长
            if max_read_time > today_read_time["todayReadSeconds"] // 60:
                read_book = read_books(headers=headers, book_url=book_url, upload_time=upload_time)
                if read_book:
                    content += f'\n【阅读时长】成功增加{upload_time}分钟阅读时长'
            else:
                content += f'\n【阅读时长】已达到设置的对大阅读时长，故不增加阅读时长'

            content += f'\n🕛耗时：%.2f秒' % (time.time() - start_time)
            print(title)
            print(content)
            # 每天 22:00 - 22:10 发送消息推送
            if qq_read_config['notify'] and beijing_datetime.hour == 22 and beijing_datetime.minute <= 10:
                notify.send(title=title, content=content, notify_mode=notify_mode)
            elif not qq_read_config['notify']:
                print('未进行消息推送，原因：未设置消息推送。如需发送消息推送，请确保配置文件的对应的脚本任务中，参数notify的值为true\n')
            elif not beijing_datetime.hour == 0:
                print('未进行消息推送，原因：没到对应的推送时间点\n')
            else:
                print('未在规定的时间范围内\n')
    else:
        print('未执行该任务，如需执行请在配置文件的对应的任务中，将参数enable设置为true\n')


def main():
    qq_read()


if __name__ == '__main__':
    main()
