# -*- coding: utf-8 -*-
from datetime import datetime


class call:
    result = False

    def __init__(self, item, sc=None, username='', icon_emoji='', channel=None, user=None, caches={}, options=None):
        if item['type'] == 'message' and item.get('subtype', None) is None:
            text = item['text']
            ts = item.get('ts', 0)

            print('{} {}> {}: {}'.format(datetime.fromtimestamp(float(ts)).strftime('%H:%M:%S'),
                                         caches.channel_ids[channel],
                                         caches.user_ids[user],
                                         text))
