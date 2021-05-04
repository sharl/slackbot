# -*- coding: utf-8 -*-
import subprocess


class call:
    """アメダス[観測地点] : アメダスでの現在の情報を表示"""
    result = False

    def __init__(self, item, sc=None, username='', icon_emoji='', channel=None, user=None, caches={}, options=None):
        ame_prefix = 'アメダス'

        if item['type'] == 'message' and item.get('subtype', None) is None:
            text = item['text']
            thread_ts = item.get('thread_ts')

            if text.startswith(ame_prefix):
                loc = text.replace(ame_prefix, '')
                amedas = subprocess.check_output(['amedas', loc]).decode('utf8').strip()
                data = {
                    'username': ame_prefix,
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
