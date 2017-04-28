#!/usr/bin/python2.7
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

# import sys
import os
import time
from datetime import datetime
import re
import json
from urlparse import urlparse
# import urllib
import subprocess
from random import random
from urllib import quote
import HTMLParser

from slackclient import SlackClient
from websocket._exceptions import WebSocketConnectionClosedException

import requests
# python 2.7.9 未満は insecure なので抑止
requests.packages.urllib3.disable_warnings()
from bs4 import BeautifulSoup

#
# Slack bot setup
#
ENVNAME = 'SLACK_TOKEN'
token = os.environ.get(ENVNAME, None)
ikachan = os.environ.get('IKACHAN', None)

username = 'hamu'
icon_emoji = ':hamster:'

# 問い合わせを減らすためのチャンネルIDキャッシュ
channel_ids = {}
# 問い合わせを減らすためのユーザIDキャッシュ
user_ids = {}


def parse(sc, data):
    for item in data:
        item_type = item.get('type')
        if item_type in ['reconnect_url', 'presence_change', 'user_typing']:
            continue

        # print('item', item)
        #
        # detect channel
        #
        channel_id = item.get('channel')
        if isinstance(channel_id, (str, unicode)) and channel_id not in channel_ids:
            chan = sc.api_call('channels.info', channel=channel_id)
            if chan['ok'] is True:
                channel_name = chan.get('channel', {}).get('name')
                if channel_name is not None:
                    channel_ids[channel_id] = channel_name
        #
        # detect user
        #
        user_id = item.get('user')
        if isinstance(user_id, (str, unicode)) and user_id not in user_ids:
            user = sc.api_call('users.info', user=user_id)
            if user['ok'] is True:
                user_name = user.get('user', {}).get('name')
                if user_name is not None:
                    user_ids[user_id] = user_name
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

            ############################################################
            # はむhelp
            ############################################################
            if text.strip().replace(' ', '') in ['help&gt;はむ', 'help＞はむ']:
                data = {
                    'username': username,
                    'icon_emoji': icon_emoji,
                    'channel': channel_id,
                    'text': '''はむ？ : スレッドに参上
<キーワード>画像＞はむ : いらすとやから画像を検索
アメダス[観測地点]＞はむ : アメダスでの現在の情報を表示''',
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

            ############################################################
            # うどん画像[＞>]はむ -> 「うどん」を取り出して画像検索
            ############################################################
            img_suffix1 = '画像＞はむ'
            img_suffix2 = '画像&gt;はむ'
            if text.endswith(img_suffix1) or text.endswith(img_suffix2):
                word = text.replace(img_suffix1, '').replace(img_suffix2, '').replace('　', '').strip()
                if len(word) == 0:
                    continue

                url = 'http://www.irasutoya.com/search?q=' + quote(word.encode('utf8'))

                r = None
                try:
                    r = requests.get(url, timeout=3)
                except Exception as e:
                    print(e)
                    continue

                if r and r.status_code == 200:
                    soup = BeautifulSoup(r.content, 'html.parser')

                    results = []
                    _as = soup.find_all(class_='boxim')
                    for _a in _as:
                        link = _a.find('a').get('href').strip()
                        pics = _a.text.strip()
                        key = 'document.write(bp_thumbnail_resize'
                        offset = 0
                        if key in pics:
                            offset = pics.index(key)
                            tmp = pics[offset:].split('"')
                            pic = tmp[1].replace('s72-c', 's400')
                            dsc = HTMLParser.HTMLParser().unescape(tmp[3])
                            attachment = {
                                'fallback': '[{}({})] {}'.format(dsc, len(_as), link),
                                'title': '[{}({})] {}'.format(word, len(_as), dsc),
                                'title_link': link,
                                'image_url': pic,
                            }
                            results.append(attachment)
                    attachment = {
                        "fallback": "{} ハズレ".format(word),
                        "title": word,
                        "text": "ハズレ"
                    }
                    if results:
                        attachment = results[int(len(results) * random())]

                data = {
                    'username': 'gazou ' + username,
                    'icon_emoji': icon_emoji,
                    'channel': channel_id,
                    'attachments': json.dumps([attachment]),
                }
                if thread_ts:
                    data['thread_ts'] = thread_ts
                sc.api_call('chat.postMessage', **data)
                time.sleep(1)

            ############################################################
            # アメダス札幌[＞>]はむ -> 「札幌」を取り出して実行
            ############################################################
            ame_prefix = 'アメダス'
            ame_suffix1 = '＞はむ'
            ame_suffix2 = '&gt;はむ'
            if text.startswith(ame_prefix) and (text.endswith(ame_suffix1) or text.endswith(ame_suffix2)):
                loc = text.replace(ame_prefix, '').replace(ame_suffix1, '').replace(ame_suffix2, '')
                amedas = subprocess.check_output(['amedas', loc]).decode('utf8').strip()
                data = {
                    'username': username,
                    'icon_emoji': icon_emoji,
                    'channel': channel_id,
                    'text': amedas,
                }
                if thread_ts:
                    data['thread_ts'] = thread_ts
                sc.api_call('chat.postMessage', **data)
                time.sleep(1)

            # URI処理
            urls = re.findall('https?://(?:[^>]+)', text)
            for url in urls:
                scheme, netloc, path, params, query, fragment = urlparse(url)
                ############################################################
                # ようつべ、ニコニコ動画のURLをirc.haun.orgに転送する
                ############################################################
                if netloc in ['www.youtube.com', 'youtu.be', 'www.nicovideo.jp', 'sp.nicovideo.jp']:
                    if channel_ids[channel_id] == 'ようつべ' and ikachan is not None:
                        res = requests.get(ikachan, params={'channel': '#ようつべ',
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


if __name__ == '__main__':
    while True:
        sc = SlackClient(token)
        try:
            if sc.rtm_connect():
                while True:
                    data = sc.rtm_read()
                    if not data:
                        time.sleep(1)
                        continue

                    parse(sc, data)
        except WebSocketConnectionClosedException:
            print('reconnecting..')
            time.sleep(1)
        except KeyboardInterrupt:
            print()
            break
