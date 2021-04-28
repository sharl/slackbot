# -*- coding: utf-8 -*-
import json
from urllib.parse import quote
from random import random
from html import unescape

import requests
from bs4 import BeautifulSoup


class call:
    """
    うどん画像 -> 「うどん」を取り出して画像検索
    """
    result = False

    def __init__(self, item, sc=None, username='', icon_emoji='', channel=None, options=None):
        img_suffix = '画像'

        if item['type'] == 'message' and item.get('subtype', None) is None:
            text = item['text']
            thread_ts = item.get('thread_ts')

            if text.endswith(img_suffix):
                word = text.replace(img_suffix, '').replace('　', '').strip()
                if len(word) == 0:
                    return

                url = 'http://www.irasutoya.com/search?q=' + quote(word.encode('utf8'))
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
