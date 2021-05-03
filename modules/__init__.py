# -*- coding: utf-8 -*-
import json
import importlib


class LoadModules:
    modules = {}
    options = {}

    def __init__(self):
        try:
            with open('config.json') as fd:
                mods = json.load(fd)
            for module in mods:
                m = importlib.import_module('modules.{}'.format(module))
                self.modules[module] = m
                self.options[module] = mods[module]
        except Exception:
            pass

    def call(self, item, sc=None, username='', icon_emoji='', channel=None, user=None, caches={}):
        for m in sorted(self.modules):
            r = self.modules[m].call(item, sc=sc, username=username, icon_emoji=icon_emoji, channel=channel, user=user, caches=caches, options=self.options[m]).result
            if r:
                break


class CACHES:
    # 問い合わせを減らすためのチャンネルIDキャッシュ
    channel_ids = {}
    # 問い合わせを減らすためのユーザIDキャッシュ
    user_ids = {}

    def __init__(self):
        pass

    def parseUID(self, sc=None, user_id=None):
        #
        # detect user
        #
        if isinstance(user_id, str) and user_id not in self.user_ids:
            user = sc.api_call('users.info', user=user_id)
            if user['ok'] is True:
                user_name = user.get('user', {}).get('name')
                if user_name is not None:
                    self.user_ids[user_id] = user_name

    def parseCID(self, sc=None, channel_id=None, user_id=None):
        #
        # detect channel
        #
        if isinstance(channel_id, str) and channel_id not in self.channel_ids:
            if channel_id.startswith('C'):
                # channel
                chan = sc.api_call('conversations.info', channel=channel_id)
                if chan['ok'] is True:
                    channel_name = chan.get('channel', {}).get('name')
                    if channel_name is not None:
                        self.channel_ids[channel_id] = channel_name
            elif channel_id.startswith('D'):
                # im
                user_name = self.user_ids.get(user_id, '???')
                self.channel_ids[channel_id] = user_name
            elif channel_id.startswith('G'):
                # group im (mpim)
                group = sc.api_call('groups.info', channel=channel_id)
                if group['ok'] is True:
                    channel_name = group.get('group', {}).get('name')
                    if channel_name is not None:
                        self.channel_ids[channel_id] = channel_name

            if channel_id not in self.channel_ids:
                self.channel_ids[channel_id] = channel_id
