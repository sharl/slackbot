# -*- coding: utf-8 -*-
import json

import requests
from bs4 import BeautifulSoup


class call:
    """台風 : 台風情報を表示
台風広域 : 広域の台風情報を表示"""
    result = False

    def __init__(self, item, sc=None, username='', icon_emoji='', channel=None, user=None, caches={}, options=None):
        url = 'https://typhoon.yahoo.co.jp/weather/jp/typhoon/'
        typhoons = {
            '台風広域': url,
            '台風': url + '?c=1',
        }
        if item['type'] == 'message' and item.get('subtype', None) is None:
            text = item['text']
            thread_ts = item.get('thread_ts')
            r = requests.get(url, timeout=10)
            if r and r.status_code == 200:
                soup = BeautifulSoup(r.content, 'html.parser')
                lis = soup.find_all('li', class_='tabView_item')
                for l in lis[2:]:
                    typhoons['台風' + l.a.text] = l.a['href']

                if text in typhoons:
                    url = typhoons[text]

                    r = requests.get(url, timeout=10)
                    if r and r.status_code == 200:
                        soup = BeautifulSoup(r.content, 'html.parser')
                        div = soup.find('div', class_='tabView_content_image')
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
