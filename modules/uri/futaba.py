# -*- coding: utf-8 -*-
import requests
import json

from bs4 import BeautifulSoup

from . import URI


class call:
    result = False

    def __init__(self, item, sc=None, username='', icon_emoji='', channel=None, user=None, caches={}, options=None):
        if item['type'] == 'message' and item.get('subtype', None) is None:
            text = item['text']
            thread_ts = item.get('thread_ts')

            uri = URI(text)
            for p in uri.parsed:
                if p.netloc.endswith('.2chan.net'):
                    url = p.geturl()
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
