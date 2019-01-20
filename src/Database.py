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
        """
        Used to store and retrieve data from the database associated with the camControl software.
        """
        # Create database connections and cursor
        self.__con = sqlite3.connect(DATABASE_NAME)
        self.__cur = self.__con.cursor()

        # Creates the table where the position the cursor is moved to and the time of the movement is stored
        self.__cur.execute('CREATE TABLE IF NOT EXISTS {} ('
                           'ID INTEGER PRIMARY KEY AUTOINCREMENT, '
                           'SessionKey INTEGER NOT NULL REFERENCES sessions(ID), '
                           'X INTEGER, '
                           'Y INTEGER, '
                           'Time REAL)'.format(TABLE_CURSOR_NAME))
        # Creates the table where sessions are stored
        self.__cur.execute('CREATE TABLE IF NOT EXISTS {} ('
                           'ID INTEGER PRIMARY KEY AUTOINCREMENT, '
                           'TimeStart REAL, '
                           'TimeEnd REAL)'.format(TABLE_SESSION_NAME))

    def create_session(self):
        """
        Used to create a session in the database.
        :return int: Returns the integer value for the ID field of the session created.
        """
        self.__cur.execute('INSERT INTO {} VALUES ('
                           'NULL, '
                           '?, '
                           'NULL)'.format(TABLE_SESSION_NAME), (time(), ))

        # Gets the ID of the session that was just created
        self.__cur.execute('SELECT MAX(ID) FROM {}'.format(TABLE_SESSION_NAME))
        # Return the session ID
        return self.__cur.fetchone()[0]

    def end_session(self, session_key: int):
        """
        Used to end (update the TimeEnd field) of the session with the same ID as the one supplied.
        :param session_key: Integer ID key for the session you desire to end.
        :return: None
        """
        self.__cur.execute("UPDATE {} SET TimeEnd = ? WHERE ID = ?".format(TABLE_SESSION_NAME),
                           (time(), session_key, ))

    def store_cursor(self, position: tuple, session_key: int):
        """
        Used to log a movement of the cursor to a certain position.
        :param position: The tuple (x, y,) position of where the cursor is being moved.
        :param session_key: The integer ID key of the session of which this movement is occurring in.
        :return: None
        """
        self.__cur.execute('INSERT INTO {} VALUES ('
                           'NULL, '
                           '?, '
                           '?, '
                           '?, '
                           '?)'.format(TABLE_CURSOR_NAME), (session_key, position[0], position[1], time(),))

    # Todo: Tweak get_sessions and get_cursor to be the same method as they could be the same:
    def get_sessions(self):
        """
        Used to get a list of all sessions that have been stored.
        :return: A list of all the sessions that have been stored.
        """
        self.__cur.execute('SELECT * FROM {}'.format(TABLE_SESSION_NAME))
        return self.__cur.fetchall()

    def get_cursor(self):
        """
        Used to get a list of all the cursor movements that have been stored.
        :return: A list of all the cursor movements that have been stored.
        """
        self.__cur.execute('SELECT * FROM {}'.format(TABLE_CURSOR_NAME))
        return self.__cur.fetchall()

    def save_changes(self):
        """
        Commits changes to database and closes connections to avoid corruption.
        :return:
        """
        self.__cur.close()
        self.__con.commit()
        self.__con.close()


if __name__ == '__main__':
    # Small manual test to make sure everything works properly:
    manager = DataBaseManager()
    # Create a session and get the key
    key = manager.create_session()
    # Log some cursor movements
    manager.store_cursor((12, 23,), key)
    manager.store_cursor((13, 24,), key)
    # Print the sessions and cursor movements to ensure that everything worked
    print("Sessions:", manager.get_sessions())
    print("Cursors:", manager.get_cursor())
