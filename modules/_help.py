# -*- coding: utf-8 -*-
class call:
    result = False

    def __init__(self, item, sc=None, username='', icon_emoji='', channel=None, user=None, caches={}, options=None):
        if item['type'] == 'message' and item.get('subtype', None) is None:
            text = item['text']
            thread_ts = item.get('thread_ts')

            if text.strip().replace(' ', '') in ['help&gt;はむ', 'help＞はむ', 'ヘルプ&gt;はむ', 'ヘルプ＞はむ']:
                data = {
                    'username': username,
                    'icon_emoji': icon_emoji,
                    'channel': channel,
                    'text': caches.doc,
                }
                if thread_ts:
                    data['thread_ts'] = thread_ts
                if sc:
                    sc.api_call('chat.postMessage', **data)
                else:
                    print(data)
                self.result = True
