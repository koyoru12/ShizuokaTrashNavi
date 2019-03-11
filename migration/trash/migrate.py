"""
trash.dbを生成するためのモジュール。
appとは別に単体で使用する。
./city.csvからcityテーブルを、./fixedreplyからfixedreplyテーブルを
./trash_opendata/*内のcsvファイルからtrashテーブルを生成する。
cityテーブルのidは、csvに指定がある場合は固定となり、指定がない場合は動的に生成される。
trashテーブルのidは、csvファイルの名前に基づき、city.csvの設定に従って設定される

```
# コマンドを実行するだけでOK
python3 migrate.py
```
"""

import sqlite3
import csv
import uuid
import glob
import re
from contextlib import closing

from settings import migrate_settings as SETTINGS
from dbconn import DatabaseConnection
from synonym import import_synonym_data

conn = DatabaseConnection.get_connection(SETTINGS['database_path'])
cursor = conn.cursor()

def import_csv(file_path):
    csv_file = open(file_path)
    return csv.DictReader(csv_file)


def import_city_data():
    cursor.execute("""
    CREATE TABLE city(
        id TEXT PRIMARY KEY,
        pref_name TEXT NOT NULL,
        city_name TEXT NOT NULL    
    )""")

    f = import_csv(SETTINGS['csv_city_path'])
    for row in f:
        data_id = str(uuid.uuid4()) if row['id'] is '' else row['id']
        pref_name = row['pref_name']
        city_name = row['city_name']
        cursor.execute("""
        INSERT INTO city(
            id, pref_name, city_name
        )VALUES(
            ?, ?, ?
        )
        """, (data_id, pref_name, city_name))

    conn.commit()
    print('city table migrated successfully')


def import_trash_data():
    def find_city_id(file_name):
        f = import_csv(SETTINGS['csv_city_path'])
        for row in f:
            if re.match('.+{}$'.format(row['file_name']), file_name):
                return row['id']
        raise Exception('FileName not Found > ' + file_name)

    cursor.execute("""
    CREATE TABLE trash(
        id TEXT PRIMARY KEY,
        city_id TEXT NOT NULL,
        name TEXT NOT NULL,
        category TEXT NOT NULL,
        note TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE trash_synonym(
        trash_id TEXT NOT NULL,
        synonym_id TEXT NOT NULL
    )
    """)
    
    cursor.execute("""
    CREATE TABLE synonym(
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL
    )
    """)

    files = glob.glob(SETTINGS['opendata_path'])
    for file_name in files:
        if not re.match('.+\.csv$', file_name):
            continue

        f = import_csv(file_name)

        for row in f:
            data_id = str(uuid.uuid4())
            city_id = find_city_id(file_name)
            name = row['name']
            category = row['category']
            note = row['note']

            cursor.execute("""
            INSERT INTO trash(
                id, city_id, name, category, note
            )VALUES(
                ?, ?, ?, ?, ?
            )
            """, (data_id, city_id, name, category, note))

    conn.commit()
    print('trash table migrated successfully')


def import_fixedreply():
    cursor.execute("""
    CREATE TABLE fixedreply(
        id TEXT PRIMARY KEY,
        message_type TEXT NOT NULL,
        match TEXT NOT NULL
    )""")

    f = import_csv(SETTINGS['csv_fixedreply_path'])
    for row in f:
        data_id = str(uuid.uuid4())
        message_type = row['message_type']
        match = row['match']
        cursor.execute("""
        INSERT INTO fixedreply(
            id, message_type, match
        )VALUES(
            ?, ?, ?
        )
        """, (data_id, message_type, match))

    conn.commit()
    print('fixedreply table migrated successfully')


if __name__ == "__main__":
    if SETTINGS['city_table']:
        cursor.execute('DROP TABLE IF EXISTS city')
        import_city_data()

    if SETTINGS['fixedreply_table']:
        cursor.execute('DROP TABLE IF EXISTS fixedreply')
        import_fixedreply()

    if SETTINGS['trash_table']:
        cursor.execute('DROP TABLE IF EXISTS trash')
        cursor.execute('DROP TABLE IF EXISTS trash_synonym')
        cursor.execute('DROP TABLE IF EXISTS synonym')
        import_trash_data()
        import_synonym_data()

    print('all operation conclude successfully!!')
