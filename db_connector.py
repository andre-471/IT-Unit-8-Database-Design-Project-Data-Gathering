import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import errorcode

load_dotenv()

user = os.environ.get('DB_USERNAME')
password = os.environ.get('DB_PASSWORD')

try:
    connection = mysql.connector.connect(
        user=user, 
        password=password, 
        host='10.8.37.226', 
        database='andrewz47_db'
    )

    cursor = connection.cursor()
    cursor.execute("show tables;")

    print(cursor.fetchall())
    
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)
else:
    connection.close()

connection.close()