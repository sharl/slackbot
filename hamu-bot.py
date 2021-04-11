#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

# import sys
import os
import time
from datetime import datetime
import re
import json
from urllib.parse import urlparse

import slackclient

import requests
from bs4 import BeautifulSoup

#
# Slack bot setup
#
token = os.environ.get('SLACK_TOKEN', None)
if not token:
    print('SLACK_TOKEN is not set')
    exit(1)

username = 'hamu'
icon_emoji = ':hamster:'

# 問い合わせを減らすためのチャンネルIDキャッシュ
channel_ids = {}
# 問い合わせを減らすためのユーザIDキャッシュ
user_ids = {}


from modules import LoadModules

modules = LoadModules()


def parse(sc, data):
    for item in data:
        item_type = item.get('type')
        if item_type in ['reconnect_url', 'presence_change', 'user_typing']:
            continue

        # print('item', item)
        #
        # detect user
        #
        user_id = item.get('user')
        if isinstance(user_id, str) and user_id not in user_ids:
            user = sc.api_call('users.info', user=user_id)
            if user['ok'] is True:
                user_name = user.get('user', {}).get('name')
                if user_name is not None:
                    user_ids[user_id] = user_name
        #
        # detect channel
        #
        channel_id = item.get('channel')
        if isinstance(channel_id, str) and channel_id not in channel_ids:
            if channel_id.startswith('C'):
                # channel
                chan = sc.api_call('conversations.info', channel=channel_id)
                if chan['ok'] is True:
                    channel_name = chan.get('channel', {}).get('name')
                    if channel_name is not None:
                        channel_ids[channel_id] = channel_name
            elif channel_id.startswith('D'):
                # im
                user_name = user_ids.get(user_id, '???')
                channel_ids[channel_id] = user_name
            elif channel_id.startswith('G'):
                # group im (mpim)
                group = sc.api_call('groups.info', channel=channel_id)
                if group['ok'] is True:
                    channel_name = group.get('group', {}).get('name')
                    if channel_name is not None:
                        channel_ids[channel_id] = channel_name

            if channel_id not in channel_ids:
                channel_ids[channel_id] = channel_id
        #
        # parse message text
        #
        if item_type == 'message' and item.get('subtype', None) is None:
            text = item['text']
            ts = item['ts']
            thread_ts = item.get('thread_ts')

            ############################################################
            print('{} {}> {}: {}'.format(datetime.fromtimestamp(float(ts)).strftime('%H:%M:%S'),
                                         channel_ids[channel_id],
                                         user_ids[user_id],
                                         text))
            ############################################################

            # ここから機能
            modules.call(text, sc=sc, username=username, icon_emoji=icon_emoji, channel=channel_id, thread_ts=thread_ts)

            ############################################################
            # はむhelp
            ############################################################
            if text.strip().replace(' ', '') in ['help&gt;はむ', 'help＞はむ', 'ヘルプ&gt;はむ', 'ヘルプ＞はむ']:
                data = {
                    'username': username,
                    'icon_emoji': icon_emoji,
                    'channel': channel_id,
                    'text': '''はむ？ : スレッドに参上
<キーワード>画像 : いらすとやから画像を検索
<カテゴリー>選んで : いらすとやから<カテゴリー>で画像検索
アメダス[観測地点] : アメダスでの現在の情報を表示
アメッシュ : アメッシュ画像を表示''',
                }
                if thread_ts:
                    data['thread_ts'] = thread_ts
                sc.api_call('chat.postMessage', **data)
                time.sleep(1)

            ############################################################
            # はむをスレッドに呼ぶ
            ############################################################
            if text in ['はむ?', 'はむ？']:
                if not thread_ts:
                    data = {
                        'username': username,
                        'icon_emoji': icon_emoji,
                        'channel': channel_id,
                        'text': 'ほえ',
                        'thread_ts': ts,
                    }
                    sc.api_call('chat.postMessage', **data)
                    time.sleep(1)

            # URI処理
            urls = re.findall('https?://(?:[^\|]+?)(?:\|.*)?>', text)
            print('urls', urls)
            for url in urls:
                url = url.rstrip('>')
                if '|' in url and url.index('|') > 0:
                    url = url.split('|')[0]
                print('url', url)
                scheme, netloc, path, params, query, fragment = urlparse(url)
                ############################################################
                # ようつべ、ニコニコ動画のURLをIRCに転送する
                ############################################################
                if netloc in ['www.youtube.com', 'm.youtube.com', 'youtu.be', 'www.nicovideo.jp', 'sp.nicovideo.jp', 'gyao.yahoo.co.jp']:
                    ikachan = os.environ.get('IKACHAN', None)
                    if channel_ids[channel_id] == 'ようつべ' and ikachan is not None:
                        res = requests.post(ikachan, data={'channel': '#ようつべ',
                                                           'message': '@{} {}'.format(user_ids[user_id], url),
                                                           })
                        data = {
                            'username': username,
                            'icon_emoji': icon_emoji,
                            'channel': channel_id,
                            'text': 'failed: {} : {}'.format(res, url),
                        }
                        if res.status_code == 200:
                            data = {
                                'username': username,
                                'icon_emoji': icon_emoji,
                                'channel': channel_id,
                                'text': 'transfer done: {}'.format(url),
                            }
                        if thread_ts:
                            data['thread_ts'] = thread_ts
                        sc.api_call('chat.postMessage', **data)
                        time.sleep(1)
                if netloc.endswith('.2chan.net'):
                    r = None
                    try:
                        r = requests.get(url, timeout=3)
                    except Exception as e:
                        print('exception', e)

                    if r and r.status_code == 200:
                        soup = BeautifulSoup(r.content, 'html.parser')
                        img = None
                        text = '\n'.join(soup.find('blockquote').strings)

                        _as = soup.find_all('a')
                        for a in _as:
                            if a.get('href').startswith('/b/src/'):
                                img = '/'.join(url.split('/')[:3]) + a.get('href')
                                break
                        if img:
                            attachment = {
                                'title_link': url,
                                'text': text,
                                'image_url': img,
                            }
                            data = {
                                'username': username,
                                'icon_emoji': icon_emoji,
                                'channel': channel_id,
                                'attachments': json.dumps([attachment]),
                            }
                            if thread_ts:
                                data['thread_ts'] = thread_ts
                            sc.api_call('chat.postMessage', **data)
                            time.sleep(1)


if __name__ == '__main__':
    while True:
        sc = slackclient.SlackClient(token)
        try:
            if sc.rtm_connect():
                while True:
                    data = sc.rtm_read()
                    if not data:
                        time.sleep(1)
                        continue

                    parse(sc, data)
        except KeyboardInterrupt:
            print()
            break
        except Exception as e:
            print('reconnecting..', e)
            time.sleep(1)
