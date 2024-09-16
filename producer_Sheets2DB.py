from flask import Flask, Response, request
from kafka import KafkaProducer
producer = KafkaProducer(bootstrap_servers='localhost:9092')
import json
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def handle_webhook():
    producer.send('Sheets2DB', request.data)
    data = json.loads(request.data.decode())
    listOFValues = data["rowData"]
    print(listOFValues)
    producer.flush()
    return 'OK'

app.run(debug=False,port=5000,host='127.0.0.1')