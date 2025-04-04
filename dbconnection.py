import atexit
import os
import signal
from typing import Generator

import mysql.connector
from dotenv import load_dotenv, find_dotenv
from mysql.connector import errorcode
from mysql.connector.abstracts import MySQLCursorAbstract


class DBConnection:
    def __init__(self):
        self.connection = None

        atexit.register(self.disconnect)
        signal.signal(signal.SIGINT, self.disconnect)
        signal.signal(signal.SIGTERM, self.disconnect)

        self.connect()

    def connect(self):
        if self.connection:
            print("Connection already exists")
            return

        if not find_dotenv():
            raise FileNotFoundError(".env file doesn't exist")

        load_dotenv()

        user = os.environ.get('DB_USERNAME')
        password = os.environ.get('DB_PASSWORD')
        name = os.environ.get('DB_NAME')

        try:
            self.connection = mysql.connector.connect(
                user=user,
                password=password,
                host='10.8.37.226',
                database=name,
                autocommit=True,
                raise_on_warnings=True
            )
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

            exit(1)

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            print("Connection closed")
        else:
            print("No connection to close")

    def query(self, query) -> list[tuple]:
        cursor: MySQLCursorAbstract
        with self.connection.cursor() as cursor:
            cursor.execute(query)

            return cursor.fetchall()

    def execute_many(self, queries: Generator) -> None:
        cursor: MySQLCursorAbstract
        with self.connection.cursor() as cursor:
            for query in queries:
                cursor.execute(query)
