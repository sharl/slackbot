# -*- coding: utf-8 -*-
import time
from datetime import datetime
import subprocess

import requests


class call:
    """黄砂 : 黄砂状況を表示"""
    result = False

    def __init__(self, item, sc=None, username='', icon_emoji='', channel=None, user=None, caches={}, options=None):
        keyword = '黄砂'

        if item['type'] == 'message' and item.get('subtype', None) is None:
            text = item['text']
            thread_ts = item.get('thread_ts')

            if text == keyword:
                now = time.time()
                fcs = datetime.fromtimestamp(now + 3 * 3600 - (now + 3 * 3600) % (3 * 3600))
                img_url = 'https://www.data.jma.go.jp/gmd/env/kosa/fcst/img/surf/jp/{}_kosafcst-s_jp_jp.png'.format(fcs.strftime('%Y%m%d%H%M'))
                r = requests.get(img_url, timeout=10)
                if r and r.status_code == 200:
                    with open('/tmp/kousa.png', 'wb') as fd:
                        fd.write(r.content)
                    with open('/tmp/kousa.png', 'rb') as fd:
                        data = {
                            'username': keyword,
                            'icon_emoji': icon_emoji,
                            'channels': channel,
                            'file': fd,
                            'filetype': 'png',
                            'filename': keyword,
                        }
                        if thread_ts:
                            data['thread_ts'] = thread_ts
                        if sc:
                            sc.api_call('files.upload', **data)
                        else:
                            subprocess.call(['convert', '/tmp/kousa.png', '/tmp/kousa.jpg'])
                            subprocess.call(['img2sixel', '/tmp/kousa.jpg'])
                        self.result = True
