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

    def call(self, item, sc=None, username='', icon_emoji='', channel=None):
        for m in self.modules:
            r = self.modules[m].call(item, sc=sc, username=username, icon_emoji=icon_emoji, channel=channel, options=self.options[m]).result
            if r:
                break
