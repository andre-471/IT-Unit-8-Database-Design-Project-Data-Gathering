import atexit
import os
import signal
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import errorcode

class DBConnection:
    def __init__(self):
        self.connection = None

        atexit.register(self.disconnect)
        signal.signal(signal.SIGINT, self.disconnect)
        signal.signal(signal.SIGTERM, self.disconnect)
        
        # self.connect()

    def connect(self):
        if self.connection:
            print("Connection already exists")
            return

        load_dotenv()

        user = os.environ.get('DB_USERNAME')
        password = os.environ.get('DB_PASSWORD')

        try:
            self.connection = mysql.connector.connect(
                user=user, 
                password=password, 
                host='10.8.37.226', 
                database='andrewz47_db'
            )
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print("Something is wrong with your user name or password")
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print("Database does not exist")
            else:
                print(err)

    def disconnect(self):
        if self.connection:
            self.connection.close()
            self.connection = None
            print("Connection closed")
        else:
            print("No connection to close")

    def execute(self, query):
        cursor = self.connection.cursor()

        cursor.execute(query)

        self.connection.commit()
        cursor.close()

