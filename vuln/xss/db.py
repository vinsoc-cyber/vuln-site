import sqlite3


def init_db():
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    c = conn.cursor()
    c.execute("""CREATE TABLE comments (id INTEGER PRIMARY KEY AUTOINCREMENT, content TEXT)""")
    conn.commit()
    return conn


_db = init_db()


def get_db():
    return _db


def reset_db():
    global _db
    _db.close()
    _db = init_db()
    return _db
