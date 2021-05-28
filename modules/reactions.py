# -*- coding: utf-8 -*-
import re


class call:
    result = False

    def __init__(self, item, sc=None, username='', icon_emoji='', channel=None, user=None, caches={}, options=None):
        if item['type'] == 'message' and item.get('subtype', None) is None:
            text = item['text']

            if isinstance(options, dict):
                for k in options:
                    if re.search(k, text):
                        data = {
                            'channel': channel,
                            'name': options[k],
                            'timestamp': item.get('ts'),
                        }
                        if sc:
                            sc.api_call('reactions.add', **data)
                        else:
                            print(data)
