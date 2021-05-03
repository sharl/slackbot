# -*- coding: utf-8 -*-
class call:
    result = False

    def __init__(self, item, sc=None, username='', icon_emoji='', channel=None, user=None, caches={}, options=None):
        # item {
        #     'ts': '1619617321.005500',
        #     'user': 'UGKNN7GD7',
        #     'type': 'reaction_added',
        #     'event_ts': '1619617321.005500',
        #     'item_user': 'UGKNN7GD7',
        #     'item': {
        #         'ts': '1619617260.005400',
        #         'channel': 'DGVNMT1EJ',
        #         'type': 'message'
        #     },
        #     'reaction': 'thinking_face'
        # }
        if item['type'] == 'reaction_added':
            if isinstance(options, list):
                if item['reaction'] in options:
                    print('options', options)
                    data = {
                        'channel': item['item']['channel'],
                        'name': item['reaction'],
                        'timestamp': item['item']['ts']
                    }
                    if sc:
                        sc.api_call('reactions.add', **data)
                    else:
                        print(data)
                    self.result = True
