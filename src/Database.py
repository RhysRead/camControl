#!/usr/bin/env python3

"""Database.py: Used to manage and edit the database for the camControl project."""

__author__ = "Rhys Read"
__copyright__ = "Copyright 2018, Rhys Read"

import sqlite3
from time import time

DATABASE_NAME = "../database.db"
TABLE_CURSOR_NAME = "cursor_log"
TABLE_SESSION_NAME = "sessions"


class DataBaseManager(object):
    def __init__(self):
        self.__con = sqlite3.connect(DATABASE_NAME)
        self.__cur = self.__con.cursor()

        # Creates the table where the position the cursor is moved to and the time of the movement is stored
        self.__cur.execute('CREATE TABLE IF NOT EXISTS {} ('
                           'ID INTEGER PRIMARY KEY AUTOINCREMENT, '
                           'SessionKey INTEGER, '
                           'X INTEGER, '
                           'Y INTEGER, '
                           'TimeStamp REAL)'.format(TABLE_CURSOR_NAME))

        self.__cur.execute('CREATE TABLE IF NOT EXISTS {} ('
                           'ID INTEGER PRIMARY KEY AUTOINCREMENT, '
                           'SessionKey INTEGER, '
                           'TimeStart REAL, '
                           'TimeEnd REAL)'.format(TABLE_SESSION_NAME))

    def create_session(self):

        session_key = 

        self.__cur.execute('INSERT INTO {} VALUES ('
                           'NULL,'
                           '?, '
                           '?, '
                           'NULL)'.format(TABLE_CURSOR_NAME), (session_key, time()))

        return session_key

    def end_session

    def store_cursor(self, position: tuple, session_key: int):
        self.__cur.execute('INSERT INTO {} VALUES ('
                           'NULL,'
                           '?, '
                           '?, '
                           '?, '
                           '?)'.format(TABLE_CURSOR_NAME), (position[0], position[1], time(), session_key,))

    def get_cursor(self):
        self.__cur.execute('SELECT * FROM {}'.format(TABLE_CURSOR_NAME))
        return self.__cur.fetchall()

    def save_changes(self):
        self.__cur.close()
        self.__con.commit()
        self.__con.close()


def drop_table(database_name: str, table_name: str):
    con = sqlite3.connect(database_name)
    con.cursor().execute("DELETE FROM {}".format(table_name))


if __name__ == '__main__':
    # Small manual test to make sure everything works properly:
    manager = DataBaseManager()
    manager.store_cursor((0, 0,))
    print(manager.get_cursor())
    manager.save_changes()
