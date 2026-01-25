import sqlite3
import time

from flask import g

DATABASE = ":memory:"


def get_db():
    db = getattr(g, "_database", None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE, check_same_thread=False)
        db.create_function("sleep", 1, lambda s: (time.sleep(float(s)) is None) and 1)
        try:
            cur = db.cursor()
            cur.execute("SELECT count(*) FROM users")
        except Exception:
            init_db(db)
    db.row_factory = sqlite3.Row
    return db


def init_db(db):
    c = db.cursor()
    c.execute(
        """CREATE TABLE users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT, status TEXT)"""
    )
    c.execute(
        "INSERT INTO users (username, password, role, status) VALUES ('admin', 's3cr3t_P@ssw0rd', 'admin', 'active')"
    )
    c.execute("INSERT INTO users (username, password, role, status) VALUES ('user', '123456', 'user', 'active')")

    c.execute("""CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price INTEGER, description TEXT)""")
    c.execute("INSERT INTO products (name, price, description) VALUES ('Quantum Core', 500, 'Powerful CPU')")
    c.execute("INSERT INTO products (name, price, description) VALUES ('Plasma Ray', 1200, 'Weapon of mass destruction')")
    c.execute("INSERT INTO products (name, price, description) VALUES ('Stealth Chip', 300, 'Invisibility module')")

    c.execute("""CREATE TABLE secrets (id INTEGER PRIMARY KEY, flag TEXT)""")
    c.execute("INSERT INTO secrets (flag) VALUES ('FLAG{SQLI_MASTER_CLASS}')")

    c.execute("""CREATE TABLE audit_logs (id INTEGER PRIMARY KEY, event TEXT, severity TEXT)""")
    c.execute("INSERT INTO audit_logs (event, severity) VALUES ('login-fail', 'low')")
    c.execute("INSERT INTO audit_logs (event, severity) VALUES ('policy-change', 'medium')")
    c.execute("INSERT INTO audit_logs (event, severity) VALUES ('admin-access', 'high')")

    db.commit()


def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_connection)
