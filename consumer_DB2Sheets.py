import gspread
import json
from google.oauth2.service_account import Credentials
from kafka import KafkaConsumer

consumer = KafkaConsumer('DB2Sheets')

scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=scopes)
client = gspread.authorize(creds)

sheet_id = "1EAasMfoDUI5CsXkcGWDVg6aWS0v5TbTIJbg9nx4LL3A"
workbook = client.open_by_key(sheet_id)
worksheet = workbook.worksheet("Values")


def find_row_index(user_id):
    column_values = worksheet.col_values(1)
    
    for row_index, value in enumerate(column_values, start=1):
        if value == str(user_id):
            return row_index  
    
    return None 


for msg in consumer:
    data = msg.value.decode('utf-8')
    event_type, data = data.split(":",1)
    message = json.loads(data)
    
    if event_type == 'DELETE' :
        user_id = message
        row_index = find_row_index(user_id)
        if row_index:
            worksheet.delete_rows(row_index)
            print(f"Deleted row with UserID {user_id}")
        else:
            print(f"UserID {user_id} not found for deletion")

    elif event_type == 'INSERT':
        new_row = message
        values = [
            new_row.get('UserID'),
            new_row.get('Username'),
            new_row.get('PhoneNo'),
            new_row.get('Email'),
            new_row.get('Gender'),
        ]
        worksheet.append_row(values)
        print(f"Inserted row with UserID {new_row.get('UserID')}")

    elif event_type == 'UPDATE':
        update_row = message
        user_id = update_row.get('UserID')
        row_index = find_row_index(user_id)
        if row_index:
            values = [
                update_row.get('Username'),
                update_row.get('PhoneNo'),
                update_row.get('Email'),
                update_row.get('Gender'),
            ]
            for i, value in enumerate(values, start=2): 
                worksheet.update_cell(row_index, i, value)
            print(f"Updated row with UserID {user_id}")
        else:
            print(f"UserID {user_id} not found for update")