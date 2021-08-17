# -*- coding: utf-8 -*-
import json

import requests
from bs4 import BeautifulSoup


class call:
    """天気図 : 天気図を表示"""
    result = False

    def __init__(self, item, sc=None, username='', icon_emoji='', channel=None, user=None, caches={}, options=None):
        url = 'https://weather.yahoo.co.jp/weather/chart/'

        if item['type'] == 'message' and item.get('subtype', None) is None:
            text = item['text']
            thread_ts = item.get('thread_ts')

            if text == '天気図':
                r = requests.get(url, timeout=10)
                if r and r.status_code == 200:
                    soup = BeautifulSoup(r.content, 'html.parser')
                    div = soup.find(id='chart-0')
                    attachment = {
                        'title': '',
                        'image_url': div.img['src'],
                    }
                    data = {
                        'username': text,
                        'icon_emoji': icon_emoji,
                        'channel': channel,
                        'attachments': json.dumps([attachment]),
                    }
                    if thread_ts:
                        data['thread_ts'] = thread_ts
                    if sc:
                        sc.api_call('chat.postMessage', **data)
                    else:
                        print(data)
