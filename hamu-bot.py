#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

import os
import time

import slackclient

from modules import LoadModules, Caches

modules = LoadModules()
caches = Caches()
caches.doc = modules.doc
#
# Slack bot setup
#
username = 'hamu'
icon_emoji = ':hamster:'


token = os.environ.get('SLACK_TOKEN', None)
if not token:
    print('SLACK_TOKEN is not set')
    exit(1)

while True:
    sc = slackclient.SlackClient(token)
    try:
        if sc.rtm_connect():
            while True:
                data = sc.rtm_read()
                if not data:
                    time.sleep(1)
                    continue

                for item in data:
                    if item['type'] in ['reconnect_url', 'presence_change', 'user_typing']:
                        continue

                    # print('item', item)
                    user_id = item.get('user')
                    caches.parseUID(sc, user_id)

                    channel_id = item.get('channel')
                    caches.parseCID(sc, channel_id, user_id)

                    modules.call(item, sc=sc, username=username, icon_emoji=icon_emoji, channel=channel_id, user=user_id, caches=caches)

    except KeyboardInterrupt:
        print()
        break
    except Exception as e:
        print('reconnecting..', e)
        time.sleep(1)
