# -*- coding: utf-8 -*-
import subprocess


class call:
    result = False

    def __init__(self, text, sc=None, username='', icon_emoji='', channel=None, thread_ts=None):
        if text == 'アメッシュ':
            amesh = subprocess.check_output(['amesh', '-c'])
            with open('/tmp/amesh.png', 'wb') as fd:
                fd.write(amesh)
            with open('/tmp/amesh.png', 'rb') as fd:
                data = {
                    'username': username,
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
