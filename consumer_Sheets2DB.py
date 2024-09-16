from kafka import KafkaConsumer
import json
from db_connection import get_database_connection
from mysql.connector import Error


consumer = KafkaConsumer('Sheets2DB')

def update_or_insert_users(record):
    """Inserts or updates user records in the database based on the given records."""
    connection = get_database_connection()
    if connection:
        try:
            cursor = connection.cursor()
            
            query = """
            INSERT INTO Users (UserID, Username, PhoneNo, Email, Gender)
            VALUES (%s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE
                Username = VALUES(Username),
                PhoneNo = VALUES(PhoneNo),
                Email = VALUES(Email),
                Gender = VALUES(Gender),
                UpdatedAt = CURRENT_TIMESTAMP;
            """
            
            user_id = record[0]
            username = record[1]
            phone_no = str(record[2])  
            email = record[3]
            gender = record[4] if record[4] != '' else "other"
            
            values = (user_id, username, phone_no, email, gender)
            cursor.execute(query, values)
            
            
            connection.commit()
            print("User records inserted or updated successfully.")
        
        except Error as e:
            print(f"Error: {e}")
        
        finally:
            cursor.close()
            connection.close()

def delete_users(user_id):
    """Deletes user records from the database based on the provided user IDs."""
    connection = get_database_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "DELETE FROM Users WHERE UserID = %s"
            cursor.execute(query, (user_id,))
            connection.commit()
            print(f"Deleted {cursor.rowcount} user(s) successfully.")
        except Error as e:
            print(f"Error: {e}")
        finally:
            cursor.close()
            connection.close()

def process_kafka_message(value):
    """Processes the Kafka message and updates/inserts records into the database."""
    data = json.loads(value)
    row_data = data.get('rowData', [])
    firstID = int(data["editedCell"].split(":")[0][1:]) - 1
    for row in row_data:
        if firstID == row[0]:
            update_or_insert_users(row)
        else:
            delete_users(firstID)
        firstID += 1   
        connection = get_database_connection()
        if connection:
            cursor = connection.cursor()
            cursor.execute("DELETE FROM event_log")  # Adjust the condition as needed
            connection.commit()
            cursor.close()
            connection.close()   
          

for msg in consumer:
    data = msg.value
    kafka_message_value_str = data.decode('utf-8')
    process_kafka_message(kafka_message_value_str)

