#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys

import sqlite3

from modules.name_history import DB_NAME

# init
if len(sys.argv) > 1:
    arg = sys.argv[1]

    con = sqlite3.connect(DB_NAME)

    if arg == 'init':
        initscript = """
DROP TABLE IF EXISTS name_history;
CREATE TABLE name_history (
id INTEGER PRIMARY KEY AUTOINCREMENT,
name STRING,            -- user.profile.real_name
email STRING,           -- user.profile.email
display_name STRING,    -- user.profile.display_name
event_ts TEXT DEFAULT (datetime(CURRENT_TIMESTAMP, 'localtime')))"""
        cur = con.cursor()
        cur.executescript(initscript)
        con.commit()

    elif sys.argv[1] == 'insert':
        cur = con.cursor()
        for i in range(0, 3):
            # insert
            cur.execute('INSERT INTO name_history (name, email, display_name) VALUES ("sharl", "sharl@haun.org", "しゃある")')
        con.commit()

    else:
        con.row_factory = sqlite3.Row
        cur = con.cursor()

        sql = "SELECT * FROM name_history WHERE name = ? OR email = ? ORDER BY id"
        cur.execute(sql, (arg, arg,))

        rows = cur.fetchall()[-10:]
        if rows:
            for r in rows:
                print(r['event_ts'], r['display_name'])
        else:
            print('{} の履歴はありません'.format(arg))

    cur.close()
    con.close()
