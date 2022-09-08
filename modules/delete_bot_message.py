# -*- coding: utf-8 -*-
class call:
    result = False

    def __init__(self, item, sc=None, username='', icon_emoji='', channel=None, user=None, caches={}, options=None):
        reaction = 'see_no_evil'
        if isinstance(options, dict) and options.get('reaction'):
            reaction = options['reaction']

        if item['type'] == 'reaction_added' and item['reaction'] == reaction:
            if username == caches.user_ids.get(item['item_user']):
                _channel = item['item']['channel']
                _ts = item['item']['ts']
                data = {
                    'channel': _channel,
                    'ts': _ts,
                }
                if sc:
                    r = sc.api_call('chat.delete', **data)

                self.result = True
