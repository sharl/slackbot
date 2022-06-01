# -*- coding: utf-8 -*-
import requests
import json


class call:
    result = False

    def __init__(self, item, sc=None, username='', icon_emoji='', channel=None, user=None, caches={}, options=None):
        if item['type'] == 'message' and item.get('subtype', None) is None:
            text = item['text']
            thread_ts = item.get('thread_ts')

            if isinstance(options, dict):
                keyword = options["keyword"]
                ouser = options["user"]
                if text == keyword and caches.user_ids[user] == ouser:
                    token = options["token"]
                    device = options["device"]

                    # https://github.com/OpenWonderLabs/SwitchBotAPI#get-device-status
                    r = requests.get("https://api.switch-bot.com/v1.0/devices/{}/status".format(device), headers={"Authorization": token}, timeout=10)
                    if r and r.status_code == 200:
                        j = json.loads(r.text)
                        temp = j.get("body").get("temperature")
                        if temp:
                            data = {
                                'username': "{}'s {}".format(ouser, keyword),
                                'icon_emoji': icon_emoji,
                                'channel': channel,
                                'text': str(temp),
                            }
                            if thread_ts:
                                data['thread_ts'] = thread_ts
                            if sc:
                                sc.api_call('chat.postMessage', **data)
                            else:
                                print(data)
                            self.result = True
