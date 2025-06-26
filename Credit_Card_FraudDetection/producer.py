# producer.py
from kafka import KafkaProducer
import json
import time
import random

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def generate_transaction():
    return {
        "features": [  # Replace with real feature values if needed
            random.uniform(0, 1) for _ in range(400)
        ],
        "timestamp": time.time()
    }

while True:
    txn = generate_transaction()
    print("📤 Sending:", txn)
    producer.send("transactions", txn)
    time.sleep(1)
