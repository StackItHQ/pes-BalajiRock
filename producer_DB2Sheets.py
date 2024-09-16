from db_connection import get_database_connection
import time
import json
from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers='localhost:9092')


def send_to_kafka(message):
    producer.send("DB2Sheets", message.encode('utf-8'))
    producer.flush()

def process_rows():
    connection = get_database_connection()
    cursor = connection.cursor(dictionary=True)
    
    try:
        cursor.execute("SELECT * FROM event_log")
        rows = cursor.fetchall()

        for row in rows:
            event_id, event_type, user_id = row 
            if row[event_type] == 'DELETE':
                send_to_kafka(row[event_type] + ":"+ str(row[user_id]))
            else:
                cursor.execute("SELECT * FROM users WHERE userID = %s", (row[user_id],))
                user_data = cursor.fetchone()
                
                column_names = [desc[0] for desc in cursor.description]
                user_data_dict = dict()
                for column in column_names:
                    if column != "UpdatedAt":
                        user_data_dict[column] = user_data[column]
                    else:
                        user_data_dict[column] = user_data[column].isoformat()
                send_to_kafka(row[event_type] + ":"+ json.dumps(user_data_dict))
        cursor.execute("DELETE FROM event_log")
        connection.commit()

    finally:
        cursor.close()
        connection.close()

while True:
    process_rows()
    time.sleep(2)