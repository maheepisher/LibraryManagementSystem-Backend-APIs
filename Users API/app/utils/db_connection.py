import mysql.connector
from mysql.connector import Error
#from dotenv import load_dotenv
import os

#load_dotenv()

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME')
        )
        if connection.is_connected():
            print("Successfully connected to the database.")
            return connection
        else:
            print("Connection established but not active.")
            return None
    except Error as e:
        print(f"Error: {e}")
        return None
