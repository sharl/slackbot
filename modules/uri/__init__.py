# -*- coding: utf-8 -*-
import re
from urllib.parse import urlparse


class URI:
    def __init__(self, text):
        self.parsed = []
        urls = re.findall('https?://(?:[^\|]+?)(?:\|.*)?>', text)
        for url in urls:
            url = url.rstrip('>')
            if '|' in url and url.index('|') > 0:
                url = url.split('|')[0]
            self.parsed.append(urlparse(url))
