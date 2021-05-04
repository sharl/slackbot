# -*- coding: utf-8 -*-
import os
import requests

from . import URI


class call:
    result = False

    def __init__(self, item, sc=None, username='', icon_emoji='', channel=None, user=None, caches={}, options=None):
        ############################################################
        # ようつべ、ニコニコ動画のURLをIRCに転送する
        ############################################################
        if item['type'] == 'message' and item.get('subtype', None) is None:
            text = item['text']
            thread_ts = item.get('thread_ts')

            uri = URI(text)
            for p in uri.parsed:
                if p.netloc in ['www.youtube.com', 'm.youtube.com', 'youtube.com', 'youtu.be', 'www.nicovideo.jp', 'sp.nicovideo.jp', 'gyao.yahoo.co.jp']:
                    ikachan = os.environ.get('IKACHAN')
                    if caches.channel_ids.get(channel) == 'ようつべ' and ikachan is not None:
                        if sc:
                            data = {
                                'channel': '#ようつべ',
                                'message': '@{} {}'.format(caches.user_ids.get(user), p.geturl()),
                            }
                            res = requests.post(ikachan, data=data)
                            data = {
                                'username': username,
                                'icon_emoji': icon_emoji,
                                'channel': channel,
                                'text': 'failed: {} : {}'.format(res, p.geturl()),
                            }
                            if res.status_code == 200:
                                data = {
                                    'username': username,
                                    'icon_emoji': icon_emoji,
                                    'channel': channel,
                                    'text': 'transfer done: {}'.format(p.geturl()),
                                }
                            if thread_ts:
                                data['thread_ts'] = thread_ts
                            sc.api_call('chat.postMessage', **data)
                        else:
                            data = {
                                'username': username,
                                'icon_emoji': icon_emoji,
                                'channel': channel,
                                'text': 'transfer done: {}'.format(p.geturl()),
                            }
                            if thread_ts:
                                data['thread_ts'] = thread_ts
                            print(data)
                        self.result = True
