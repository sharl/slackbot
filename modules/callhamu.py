# -*- coding: utf-8 -*-
class call:
    result = False

    def __init__(self, item, sc=None, username='', icon_emoji='', channel=None, user=None, caches={}, options=None):
        ############################################################
        # はむをスレッドに呼ぶ
        ############################################################
        if item['type'] == 'message' and item.get('subtype', None) is None:
            text = item['text']
            thread_ts = item.get('thread_ts')

            if text in ['はむ?', 'はむ？']:
                if not thread_ts:
                    data = {
                        'username': username,
                        'icon_emoji': icon_emoji,
                        'channel': channel,
                        'text': 'ほえ',
                        'thread_ts': item.get('ts'),
                    }
                    if sc:
                        sc.api_call('chat.postMessage', **data)
                    else:
                        print(data)
                self.result = True
