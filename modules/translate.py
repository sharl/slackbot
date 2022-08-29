# -*- coding: utf-8 -*-
import requests
from urllib.parse import quote


class call:
    """英訳<text> : 日本語を英語に翻訳
和訳<text> : 英語を日本語に翻訳"""
    result = False

    def __init__(self, item, sc=None, username='', icon_emoji='', channel=None, user=None, caches={}, options=None):
        if item['type'] == 'message' and item.get('subtype', None) is None:
            text = item['text']
            thread_ts = item.get('thread_ts')
            keyword = '英訳'
            if text.startswith(keyword):
                r = requests.get('http://api.excelapi.org/translate/jaen?text=' + quote(text.replace(keyword, '', 1)), timeout=30)
                if r and r.status_code == 200:
                    data = {
                        'username': keyword,
                        'icon_emoji': icon_emoji,
                        'channel': channel,
                        'text': r.text,
                    }
                    if thread_ts:
                        data['thread_ts'] = thread_ts
                    if sc:
                        sc.api_call('chat.postMessage', **data)
                    else:
                        print(data)
                    self.result = True
            keyword = '和訳'
            if text.startswith(keyword):
                r = requests.get('http://api.excelapi.org/translate/enja?text=' + quote(text.replace(keyword, '', 1)), timeout=30)
                if r and r.status_code == 200:
                    data = {
                        'username': keyword,
                        'icon_emoji': icon_emoji,
                        'channel': channel,
                        'text': r.text,
                    }
                    if thread_ts:
                        data['thread_ts'] = thread_ts
                    if sc:
                        sc.api_call('chat.postMessage', **data)
                    else:
                        print(data)
                    self.result = True
