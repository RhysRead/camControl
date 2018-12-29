#!/usr/bin/env python3

"""Database.py: Used to manage and edit the database for the camControl project."""

__author__ = "Rhys Read"
__copyright__ = "Copyright 2018, Rhys Read"

import sqlite3


class DataBaseManager(object):
    def __init__(self):
        self.__con = sqlite3.connect('../database.db')
        self.__cur = self.__con.cursor()

        # Creates the table where the position the cursor is moved to and the time of the movement is stored
        self.__cur.execute('CREATE TABLE IF NOT EXISTS cursor_log ('
                           'ID INTEGER PRIMARY KEY AUTOINCREMENT, '
                           'X INTEGER, '
                           'Y INTEGER, '
                           'TimeStamp DATETIME DEFAULT CURRENT_TIMESTAMP)')

    def store_cursor(self, position: tuple):
        self.__cur.execute('INSERT INTO cursor_log ('
                           '?, '
                           '?)', (position[0], position[1], ))

    def get_cursor(self):
        self.__cur.execute('SELECT * FROM cursor_log')
        return self.__cur.fetchall()


def wipe_database(database_name: str):
    con = sqlite3.connect(database_name)
    con.cursor().execute('DELETE * FROM *')


if __name__ == '__main__':
    manager = DataBaseManager()
    manager.store_cursor((0, 0,))
    manager.get_cursor()
    wipe_database('../database.db')
