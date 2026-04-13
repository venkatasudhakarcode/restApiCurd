import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="studentdb"
        )

        if conn.is_connected():
            print("Connected to DataBase")
            return conn
        
    except Error as e:
        print("Error Occured While Connecting DataBase:",e)
        return None