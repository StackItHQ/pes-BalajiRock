import mysql.connector
from mysql.connector import Error

def get_database_connection():
    """Establishes and returns a database connection."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='4321',
            database='SyncSheetsDB'
        )
        return connection
    except Error as e:
        print(f"Error: {e}")
        return None
