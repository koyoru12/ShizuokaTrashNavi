import sqlite3


DB_NAME = 'user.db'

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS user')

cursor.execute("""
CREATE TABLE user(
    id TEXT PRIMARY KEY,
    city_id TEXT
)
""")

print('operation success!')