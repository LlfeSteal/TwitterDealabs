import pickle
import sqlite3

def create_tables(conn):
    cursor = conn.cursor()

    cursor.execute('CREATE TABLE IF NOT EXISTS threads (id INTEGER PRIMARY KEY)')
    cursor.execute('CREATE TABLE IF NOT EXISTS tokens (token_name VARCHAR(255) PRIMARY KEY, token_value VARCHAR(255))')

    conn.commit()
    cursor.close()

class StorageService:
    def __init__(self):
        self.conn = sqlite3.connect('threads.db')
        create_tables(self.conn)

    def get_stored_thread_ids(self):
        cursor = self.conn.cursor()
        cursor.execute('SELECT id FROM threads')
        ids = cursor.fetchall()
        cursor.close()
        return list(map(lambda obj: obj[0], ids))

    def store_thread_ids(self, thread_ids):
        cursor = self.conn.cursor()
        for thread_id in thread_ids:
            cursor.execute("INSERT INTO threads (id) VALUES (" + str(thread_id) + ")")
        self.conn.commit()
        cursor.close()

    def get_stored_token_value(self, name):
        cursor = self.conn.cursor()
        cursor.execute("SELECT token_value FROM tokens WHERE token_name='{name}'".format(name=name))
        id = cursor.fetchone()
        cursor.close()
        return id[0] if id else None

    def store_token(self, name, value):
        cursor = self.conn.cursor()
        cursor.execute("REPLACE INTO `tokens` (token_name, token_value) VALUES ('{name}', '{value}');".format(name=name, value=value))
        self.conn.commit()
        cursor.close()

    def __del__(self):
        self.conn.close()
