# -*- coding: utf-8 -*-
import json
from urllib.parse import quote
from random import random
from html import unescape

import requests
from bs4 import BeautifulSoup


class call:
    """[カテゴリー]選んで : カテゴリーから画像検索
選んでヘルプ : カテゴリー一覧を表示
選んでhelp : カテゴリー一覧を表示"""
    result = False

    def __init__(self, item, sc=None, username='', icon_emoji='', channel=None, user=None, caches={}, options=None):
        category_suffix = '選んで'

        if item['type'] == 'message' and item.get('subtype', None) is None:
            text = item['text']
            thread_ts = item.get('thread_ts')

            if text.endswith(category_suffix):
                category = text.replace(category_suffix, '').strip()
                if len(category) == 0:
                    return

                url = 'https://www.irasutoya.com/search/label/' + quote(category.encode('utf8')) + '?max-results=200'
                r = None
                try:
                    r = requests.get(url, timeout=3)
                except Exception as e:
                    print(e)
                    return

                if r and r.status_code == 200:
                    soup = BeautifulSoup(r.content, 'html.parser')

                    results = []
                    _as = soup.find_all(class_='boxim')
                    for _a in _as:
                        tmp = str(_a.find('a')).split('"')
                        link = tmp[1].strip()
                        pic = tmp[5].replace('s72-c', 's400')
                        dsc = unescape(tmp[7])
                        attachment = {
                            'fallback': '[{}({})] {}'.format(dsc, len(_as), link),
                            'title': '[{}({})] {}'.format(category, len(_as), dsc),
                            'title_link': link,
                            'image_url': pic,
                        }
                        results.append(attachment)

                    attachment = {
                        "fallback": "{} ハズレ".format(category),
                        "title": category,
                        "text": "ハズレ"
                    }
                    if results:
                        attachment = results[int(len(results) * random())]

                    data = {
                        'username': username,
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

                    self.result = True
            elif text in ['選んでhelp', '選んでヘルプ']:
                r = None
                try:
                    r = requests.get('https://www.irasutoya.com/', timeout=3)
                except Exception as e:
                    print(e)
                    return

                if r and r.status_code == 200:
                    soup = BeautifulSoup(r.content, 'html.parser')
                    results = []

                    _adir = soup.find_all('a', dir='ltr')
                    for a in _adir:
                        results.append(a.text)
                    data = {
                        'username': username,
                        'icon_emoji': icon_emoji,
                        'channel': channel,
                        'text': '```{}```'.format(' '.join(results)),
                    }
                    if thread_ts:
                        data['thread_ts'] = thread_ts
                    if sc:
                        sc.api_call('chat.postMessage', **data)
                    else:
                        print(data)

                    self.result = True
