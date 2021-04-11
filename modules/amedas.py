# -*- coding: utf-8 -*-
import subprocess


class call:
    result = False

    def __init__(self, text, sc=None, username='', icon_emoji='', channel=None, thread_ts=None):
        ame_prefix = 'アメダス'

        if text.startswith(ame_prefix):
            loc = text.replace(ame_prefix, '')
            amedas = subprocess.check_output(['amedas', loc]).decode('utf8').strip()
            data = {
                'username': username,
                'icon_emoji': icon_emoji,
                'channel': channel,
                'text': amedas,
            }
            if thread_ts:
                data['thread_ts'] = thread_ts
            if sc:
                sc.api_call('chat.postMessage', **data)
            else:
                print(data)

            self.result = True
