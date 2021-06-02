# -*- coding: utf-8 -*-
import re
import json
from random import random
import time


class timer:
    timer = 0


class call:
    result = False

    def __init__(self, item, sc=None, username='', icon_emoji='', channel=None, user=None, caches={}, options=None):
        if item['type'] == 'message' and item.get('subtype', None) is None:
            text = item['text']
            thread_ts = item.get('thread_ts')

            now = time.time()
            for k in options['keywords']:
                if re.search(k, text) and now - timer.timer > options['interval']:
                    images = options['keywords'][k]
                    attachment = {
                        'title': '',
                        'image_url': images[int(random() * len(images))],
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

                    timer.timer = now
                    return
