"""
各市町村のデータを一度全部DBに入れる
類語検索する
ヒットした類語をsynonymテーブルに入れる
類語とごみデータを結びつけてtrash-synonymテーブルに入れる
"""

"""
wordからwordidを取得
senseからwordidをキーにしてsynsetを取得
senseからsynsetをキーにしてwordidを取得
"""


import re
import uuid

from settings import migrate_settings as SETTINGS
from dbconn import DatabaseConnection


wn_conn = DatabaseConnection.get_connection(SETTINGS['wndatabase_path'])
wn_cursor = wn_conn.cursor()

trash_conn = DatabaseConnection.get_connection(SETTINGS['database_path'])
trash_cursor = trash_conn.cursor()

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

        for synonym in find_synonym(trash_name):
            insert_synonym(trash['id'], synonym)
    trash_conn.commit()
    print('synonym table migrated successfully')


def insert_synonym(trash_id, synonym):
    synonym_id = ''

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


def find_synonym(word):
    def find_words_by_name(lemma):
        wn_cursor.execute("""
        SELECT * FROM word WHERE lemma = ?
        """, (lemma,))
        return wn_cursor.fetchall()
    
    def find_word_by_wordid(word_id):
        wn_cursor.execute("""
        SELECT * FROM word WHERE wordid = ?
        """, (word_id,))
        return wn_cursor.fetchone()
    
    def find_synsets_by_wordid(word_id, lang='jpn'):
        wn_cursor.execute("""
        SELECT * FROM sense
            WHERE wordid = ?
            AND lang = ?
        """, (word_id, lang))
        return wn_cursor.fetchall()
    
    def find_senses_by_synset(synset, lang='jpn', word_id=''):
        wn_cursor.execute("""
        SELECT * FROM sense
            WHERE synset = ?
            AND lang = ?
            AND wordid != ?
        """, (synset, lang, word_id))
        return wn_cursor.fetchall()

    def append_result(word):
        nonlocal result
        for w in result:
            if word == w:
                return
        result.append(word)

    result = []
    words = find_words_by_name(word)
    for word in words:
        synsets = find_synsets_by_wordid(word['wordid'])
        for synset in synsets:
            senses = find_senses_by_synset(synset['synset'], word_id=word['wordid'])
            for sense in senses:
                word_res = find_word_by_wordid(sense['wordid'])
                append_result(word_res['lemma'])

    return result