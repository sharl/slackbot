# -*- coding: utf-8 -*-
import json
import importlib


class LoadModules:
    modules = {}

    def __init__(self):
        try:
            with open('config.json') as fd:
                mods = json.load(fd)
            for module in mods:
                m = importlib.import_module('modules.{}'.format(module))
                self.modules[module] = m
        except Exception:
            pass

    def call(self, text, sc=None, username='', icon_emoji='', channel=None, thread_ts=None):
        for m in self.modules:
            r = self.modules[m].call(text, sc=sc, username=username, icon_emoji=icon_emoji, channel=channel, thread_ts=thread_ts).result
            if r:
                break
