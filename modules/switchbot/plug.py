# -*- coding: utf-8 -*-
import requests


class call:
    result = False

    def __init__(self, item, sc=None, username='', icon_emoji='', channel=None, user=None, caches={}, options=None):
        if item['type'] == 'message' and item.get('subtype', None) is None:
            text = item['text']

            if isinstance(options, dict):
                on = options['on']
                off = options['off']
                if text == on or text == off:
                    token = options['token']
                    device = options['device']
                    commands = {
                        on: 'turnOn',
                        off: 'turnOff',
                    }
                    command = commands[text]

                    # https://github.com/OpenWonderLabs/SwitchBotAPI#send-device-control-commands
                    requests.post('https://api.switch-bot.com/v1.0/devices/{}/commands'.format(device),
                                  headers={'Authorization': token},
                                  json={
                                      'command': command,
                                      'parameter': 'default',
                                      'commandType': 'command',
                                  },
                                  timeout=10)
                    self.result = True
