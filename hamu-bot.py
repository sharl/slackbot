#!/usr/bin/python3
# -*- coding: utf-8 -*-
from __future__ import print_function
from __future__ import unicode_literals

# import sys
import os
import time

import slackclient

#
# Slack bot setup
#
username = 'hamu'
icon_emoji = ':hamster:'


from modules import LoadModules, CACHES

modules = LoadModules()
caches = CACHES()
caches.doc = modules.doc


def parse(sc, data):
    for item in data:
        item_type = item.get('type')
        if item_type in ['reconnect_url', 'presence_change', 'user_typing']:
            continue

        # print('item', item)
        #
        # detect user
        #
        user_id = item.get('user')
        caches.parseUID(sc, user_id)
        #
        # detect channel
        #
        channel_id = item.get('channel')
        caches.parseCID(sc, channel_id, user_id)
        #
        # 機能
        #
        modules.call(item, sc=sc, username=username, icon_emoji=icon_emoji, channel=channel_id, user=user_id, caches=caches)


if __name__ == '__main__':
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

                    parse(sc, data)
        except KeyboardInterrupt:
            print()
            break
        except Exception as e:
            print('reconnecting..', e)
            time.sleep(1)
