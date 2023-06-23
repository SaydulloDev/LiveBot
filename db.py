import sqlite3


def db_config():
    with sqlite3.connect('db.sqlite3') as connection:
        try:
            cursor = connection.cursor()
            cursor.execute('CREATE TABLE users ('
                           'id INTEGER PRIMARY KEY,'
                           'chat_id INTEGER NOT NULL UNIQUE ,'
                           'first_name VARCHAR(255)'
                           ')')
        except Exception as e:
            return f'Error <b>{e}</b>'
        else:
            return True


def add_user(chat_id, first_name, last_name):
    try:
        with sqlite3.connect('db.sqlite3') as connection:
            cursor = connection.cursor()
            cursor.execute('INSERT INTO users (chat_id,first_name) VALUES (?,?)',
                           (chat_id, first_name))
    except Exception as e:
        return f'Failed to add user {e}'


def get_user(chat_id):
    try:
        with sqlite3.connect('db.sqlite3') as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT chat_id FROM users WHERE chat_id = ?', (chat_id,))
            result = cursor.fetchall()
            if not result:
                return False
            else:
                return True
    except Exception as e:
        return f'Failed to get user {e}'


def get_full_info():
    try:
        with sqlite3.connect('db.sqlite3') as connection:
            cursor = connection.cursor()
            cursor.execute('SELECT first_name, chat_id FROM users')
            result = cursor.fetchall()
            return result
    except Exception as e:
        return f'Error {e}'
