# consumer.py
from kafka import KafkaConsumer
import json
import numpy as np
import joblib
import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

load_dotenv()






def send_email_alert(data):
    sender = os.getenv('EMAIL_USER')
    password = os.getenv('EMAIL_PASS')
    
    receiver = 'donamarangattu@gmail.com'
     

    msg = MIMEText(f"⚠️ Fraudulent Transaction Detected!\n\nDetails:\n{data}")
    msg['Subject'] = '🚨 Fraud Alert!'
    msg['From'] = sender
    msg['To'] = receiver

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender, password)
            server.send_message(msg)
            print("📧 Email alert sent.")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")


# Load saved model and scaler
model = joblib.load("fraud_model.joblib")
scaler = joblib.load("scaler.joblib")

# Kafka consumer
consumer = KafkaConsumer(
    'transactions',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='earliest',
    group_id='fraud-group'
)

print("📡 Listening for transactions...")

for message in consumer:
    try:
        transaction = message.value
        print("📥 Received:", transaction)

        features = np.array([transaction["features"]])
        features_scaled = scaler.transform(features)
        prediction = model.predict(features_scaled)[0]

        if prediction == 1:
            print("🚨 Fraud detected!")
            send_email_alert(transaction)
        else:
            print("✅ Transaction is normal.")
    except Exception as e:
        print("⚠️ Error:", e)
