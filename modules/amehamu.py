# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from urllib.parse import quote
import subprocess

import requests
from bs4 import BeautifulSoup


class call:
    result = False

    def __init__(self, text, sc=None, username='', icon_emoji='', channel=None, thread_ts=None):
        keyword = 'あめはむ'
        zoom = '10'

        if text.startswith(keyword):
            loc = text.replace(keyword, '')
            if ' ' in loc:
                loc, zoom = loc.split(' ')
            if not loc:
                loc = '下呂'
                zoom = '3'
            loc = loc.strip()
            zoom = zoom.strip()
            url = 'https://www.geocoding.jp/api/?q=' + quote(loc.encode('utf8'))
            r = requests.get(url, timeout=10)
            if r and r.status_code == 200:
                print(r.text.strip())
                root = ET.fromstring(r.text)
                lat = None
                lng = None
                if root.find('./error') is None:
                    lat = root.find('./coordinate/lat').text
                    lng = root.find('./coordinate/lng').text

                if lat and lng:
                    r = requests.get('https://weather.yahoo.co.jp/weather/zoomradar/?lat={}&lon={}&z={}'.format(lat, lng, zoom))
                    if r and r.status_code == 200:
                        soup = BeautifulSoup(r.content, 'html.parser')
                        og_images = soup.find_all('meta', property="og:image")
                        if len(og_images) == 0:
                            return
                        img_url = og_images[0].get('content').replace('600x600', '300x300')
                        print(img_url)
                        r = requests.get(img_url, timeout=3)
                        if r and r.status_code == 200:
                            with open('/tmp/amehamu.png', 'wb') as fd:
                                fd.write(r.content)
                            with open('/tmp/amehamu.png', 'rb') as fd:
                                data = {
                                    'username': keyword,
                                    'icon_emoji': icon_emoji,
                                    'channels': channel,
                                    'file': fd,
                                    'filetype': 'png',
                                    'filename': loc,
                                }
                                if thread_ts:
                                    data['thread_ts'] = thread_ts
                                if sc:
                                    sc.api_call('files.upload', **data)
                                else:
                                    subprocess.call(['img2sixel', '/tmp/amehamu.png'])
                                self.result = True
                else:
                    data = {
                        'username': keyword,
                        'icon_emoji': icon_emoji,
                        'channels': channel,
                        'text': loc + 'は見つからなかったよ',
                    }
                    if thread_ts:
                        data['thread_ts'] = thread_ts
                    if sc:
                        sc.api_call('chat.postMessage', **data)
                    else:
                        print(data)
            else:
                data = {
                    'username': keyword,
                    'icon_emoji': icon_emoji,
                    'channels': channel,
                    'text': loc + 'のスポット情報取得に失敗しました',
                }
                if thread_ts:
                    data['thread_ts'] = thread_ts
                if sc:
                    sc.api_call('chat.postMessage', **data)
                else:
                    print(data)
