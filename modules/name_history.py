# -*- coding: utf-8 -*-
import sqlite3

DB_NAME = './conf/name_history.db'


class call:
    """<キーワード>履歴 : 履歴を表示"""
    result = False

    def __init__(self, item, sc=None, username='', icon_emoji='', channel=None, user=None, caches={}, options=None):
        suffix = '履歴'

        if item['type'] == 'message' and item.get('subtype', None) is None:
            text = item['text']
            thread_ts = item.get('thread_ts')

            if text.endswith(suffix):
                keyword = text.replace(suffix, '')

                # キーワードを置き換え
                alias = ''
                if isinstance(options, dict):
                    for k in options:
                        if keyword == k:
                            keyword = options[k]
                            alias = k
                            break
                if not alias:
                    alias = keyword
                # 履歴検索・表示
                con = sqlite3.connect(DB_NAME)
                con.row_factory = sqlite3.Row
                cur = con.cursor()
                sql = 'SELECT * FROM name_history WHERE name = ? OR email = ? ORDER BY id'
                cur.execute(sql, (keyword, keyword,))

                rows = cur.fetchall()[-10:]
                if rows:
                    messages = []
                    for r in rows:
                        messages.append('{} {}'.format(r['event_ts'], r['display_name']))
                    message = '```{}```'.format('\n'.join(messages))
                else:
                    message = '"{}" の履歴はありません'.format(alias)
                data = {
                    'username': alias + suffix,
                    'icon_emoji': icon_emoji,
                    'channel': channel,
                    'text': message,
                }
                if thread_ts:
                    data['thread_ts'] = thread_ts
                if sc:
                    sc.api_call('chat.postMessage', **data)
                else:
                    print(data)

                self.result = True

        elif item['type'] == 'user_change':
            real_name = item['user']['real_name']
            display_name = item['user']['profile']['display_name']
            email = item['user']['profile']['email']

            con = sqlite3.connect(DB_NAME)
            cur = con.cursor()
            cur.execute('INSERT INTO name_history (name, email, display_name) VALUES (?, ?, ?)', (real_name, email, display_name,))
            con.commit()
            con.close()
