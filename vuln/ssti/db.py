import sqlite3

from flask import g

DATABASE = ":memory:"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE, check_same_thread=False)
        try:
            cur = db.cursor()
            cur.execute("SELECT count(*) FROM users")
        except Exception:
            init_db(db)
    db.row_factory = sqlite3.Row
    return db


def init_db(db):
    c = db.cursor()
    c.execute("""CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, role TEXT)""")
    c.execute("INSERT INTO users (username, role) VALUES ('admin', 'administrator')")
    c.execute("INSERT INTO users (username, role) VALUES ('guest', 'visitor')")
    c.execute("INSERT INTO users (username, role) VALUES ('user', 'regular')")
    c.execute("""CREATE TABLE templates (id INTEGER PRIMARY KEY AUTOINCREMENT, label TEXT, body TEXT)""")
    db.commit()


def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_connection)
