"""
trash.dbを生成するためのモジュール。
appとは別に単体で使用する。
./city.csvからcityテーブルを、./fixedreplyからfixedreplyテーブルを
./trash_opendata/*内のcsvファイルからtrashテーブルを生成する。
cityテーブルのidは、csvに指定がある場合は固定となり、指定がない場合は動的に生成される。

```
# コマンドを実行するだけでOK
python3 migrate.py
```
"""

import sqlite3
import csv
import uuid
import glob
from contextlib import closing


DB_NAME = 'trash.db'
CSV_CITY = 'city.csv'
CSV_FIXEDREPLY = 'fixedreply.csv'
OPENDATA_DIR = './trash_opendata/*'


with closing(sqlite3.connect(DB_NAME)) as conn:
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('DROP TABLE IF EXISTS city')
    cursor.execute('DROP TABLE IF EXISTS trash')
    cursor.execute('DROP TABLE IF EXISTS fixedreply')


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

        f = import_csv(CSV_CITY)
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
    

    def import_trash_data():
        cursor.execute("""
        CREATE TABLE trash(
            id TEXT PRIMARY KEY,
            city_id TEXT NOT NULL,
            name TEXT NOT NULL,
            category TEXT NOT NULL,
            note TEXT
        )
        """)

        files = glob.glob(OPENDATA_DIR)
        for file_name in files:
            f = import_csv(file_name)

            for row in f:
                data_id = str(uuid.uuid4())
                city_id = row['city_id']
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


    def import_fixedreply():
        cursor.execute("""
        CREATE TABLE fixedreply(
            id TEXT PRIMARY KEY,
            message_type TEXT NOT NULL,
            match TEXT NOT NULL
        )""")

        f = import_csv(CSV_FIXEDREPLY)
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


    if __name__ == "__main__":
        import_city_data()
        import_trash_data()
        import_fixedreply()
        
