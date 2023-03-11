import os
import sqlite3

from utils.date import date

class Database(object):
    """
        database functions
    """
    # Connect to the database
    global CONNECTION, CURSOR
    CONNECTION = sqlite3.connect("database/database.db", check_same_thread=False)
    CURSOR = CONNECTION.cursor()

    def __init__(self) -> None:
        pass
    
    # Handle session table
    def add_session(self, session_id: str) -> None:
        """
            add new session id
        """
        sql = "INSERT INTO sessions VALUES ('%s', '%s');" % (session_id, date())
        CURSOR.execute(sql)
        CONNECTION.commit()

    def get_sessions(self) -> dict:
        """
            Returns all saved sessions
        """
        sql = "SELECT * FROM sessions;"
        responce = CURSOR.execute(sql).fetchall()

        return responce

    def delete_session(self, session_id: str) -> None:
        """
            Delete a spicific session 
            from the datebase
        """
        sql = "DELETE FROM sessions WHERE session_id = '%s'" % session_id
        CURSOR.execute(sql)
        CONNECTION.commit()

