import re
import csv
import uuid
from dbconn import DatabaseConnection

from settings import migrate_settings as SETTINGS


trash_conn = DatabaseConnection.get_connection(SETTINGS['database_path'])
trash_cursor = trash_conn.cursor()

def import_csv(file_path):
    csv_file = open(file_path)
    return csv.DictReader(csv_file)

def import_synonym_data():
    count_exist = 0
    count_nonexist = 0
    count_synosym = 0
    trash_list = trash_cursor.execute('SELECT * FROM trash').fetchall()
    for trash in trash_list:
        # 括弧書きがあるものをストリップする
        trash_name = trash['name']
        m = re.match('([^\(（]+)[\(（]', trash_name)
        trash_name = trash_name if m == None else m.group(1)

        synlist = find_synonym(trash_name)
        for synonym in synlist:
            insert_synonym(trash['id'], synonym)

    trash_conn.commit()
    print('synonym table migrated successfully')

def find_synonym(trash_name):
    result = []
    synonym_csv = import_csv(SETTINGS['csv_synonym_path'])
    for row in synonym_csv:
        if trash_name == row['trash_name']:
            result.append(row['synonym'])
    return result


def insert_synonym(trash_id, synonym):
    trash_cursor.execute('SELECT id FROM synonym WHERE name = ?', (synonym,))
    row = trash_cursor.fetchone()
    if row == None:
        # synonymがなければ登録する
        synonym_id = str(uuid.uuid4())
        trash_cursor.execute("""
        INSERT INTO synonym(
            id, name
        )VALUES(
            ?, ?
        ) """, (synonym_id, synonym))
    else:
        synonym_id = row['id']
        
    # trash_synonymの登録
    trash_cursor.execute("""
    INSERT INTO trash_synonym(
        trash_id, synonym_id
    )VALUES(
        ?, ?
    )
    """, (trash_id, synonym_id))
