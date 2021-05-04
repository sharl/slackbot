# -*- coding: utf-8 -*-
import subprocess


class call:
    """アメッシュ : アメッシュ画像を表示"""
    result = False

    def __init__(self, item, sc=None, username='', icon_emoji='', channel=None, user=None, caches={}, options=None):
        keyword = 'アメッシュ'

        if item['type'] == 'message' and item.get('subtype', None) is None:
            text = item['text']
            thread_ts = item.get('thread_ts')

            if text == keyword:
                amesh = subprocess.check_output(['amesh', '-c'])
                with open('/tmp/amesh.png', 'wb') as fd:
                    fd.write(amesh)
                with open('/tmp/amesh.png', 'rb') as fd:
                    data = {
                        'username': keyword,
                        'icon_emoji': icon_emoji,
                        'channels': channel,
                        'file': fd,
                        'filetype': 'png',
                    }
                    if thread_ts:
                        data['thread_ts'] = thread_ts
                    if sc:
                        sc.api_call('files.upload', **data)
                    else:
                        subprocess.call(['img2sixel', '/tmp/amesh.png'])

                    self.result = True
