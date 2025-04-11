import sqlite3


def db_connect():
    return sqlite3.connect("instance/app.db")
