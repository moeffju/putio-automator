import os
import pathlib
import sqlite3

import appdirs

from putio_automator import APP_AUTHOR, APP_NAME

user_data_dir = appdirs.user_data_dir(APP_NAME, APP_AUTHOR)
database_path = os.path.join(user_data_dir, 'downloads.db')


def with_db(func):
    if not os.path.exists(database_path):
        pathlib.Path(user_data_dir).mkdir(parents=True, exist_ok=True)
        open(database_path, 'w').close()

    with sqlite3.connect(database_path) as connection:
        func(connection)


def create_db():
    def func(connection):
        c = connection.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS torrents (name CHARACTER VARYING PRIMARY KEY, size INTEGER, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
        c.execute('CREATE TABLE IF NOT EXISTS downloads (id INTEGER PRIMARY KEY, name CHARACTER VARYING, size INTEGER, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)')
    with_db(func)
