# -*- coding: utf-8 -*-
from random import random

import requests
from bs4 import BeautifulSoup


class call:
    """かしはむ[キーワード] : 歌詞を検索"""
    wake = 'かしはむ'
    result = False

    def __init__(self, item, sc=None, username='', icon_emoji='', channel=None, user=None, caches={}, options=None):
        if item['type'] == 'message' and item.get('subtype', None) is None:
            text = item['text']
            thread_ts = item.get('thread_ts')

            if text.startswith(self.wake):
                keyword = text.replace(self.wake, '').encode('shift_jis').strip()

                res = requests.post('http://phrase.utamap.com/searchkasi_phrase.php', data={'pattern': 3, 'word': keyword}, timeout=10)
                if res and res.status_code == 200:
                    soup = BeautifulSoup(res.content, 'html.parser')
                    tds = soup.find_all('td', class_='ct160')
                    _as = []
                    for td in tds:
                        a = td.find('a')
                        if a:
                            _as.append(a['href'])
                    if _as:
                        uri = _as[int(len(_as) * random())]
                        print(uri)
                        res = requests.get(uri, timeout=10)
                        if res and res.status_code == 200:
                            soup = BeautifulSoup(res.content, 'html.parser')
                            title = soup.find('td',  class_='kasi1')
                            lyric = soup.find('td', class_='kasi_honbun')
                            singer = soup.find_all('td', class_='pad5x10x0x10')
                            lyrics = [
                                str(lyric).split('\n')[1].replace('<br/>', '\n'),
                                '\n\n',
                                '『{}』{}'.format(title.text, singer[-1].text),
                            ]
                            content = ''.join(lyrics)
                            data = {
                                'channels': channel,
                                'content': content,
                                'filetype': 'text',
                            }
                            if thread_ts:
                                data['thread_ts'] = thread_ts
                            if sc:
                                sc.api_call('files.upload', **data)
                            else:
                                print(content)

                            self.result = True
