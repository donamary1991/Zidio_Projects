# 💳 Credit Card Fraud Detection

A machine learning-based system to detect fraudulent credit card transactions in real-time. The project includes both offline and real-time detection pipelines using Kafka, SMOTE, XGBoost, and email alerts.

---

## 📌 Features

- 🧠 **ML Models**: Trained using XGBoost, Random Forest, and Logistic Regression
- ⚖️ **SMOTE**: Handles class imbalance by generating synthetic minority samples
- 🔍 **Anomaly Detection**: Optional unsupervised module (e.g., Isolation Forest, Autoencoder)
- 🛰️ **Real-time Monitoring**: Kafka producer-consumer pipeline
- 📬 **Email Alerts**: Auto-emailing for suspected fraudulent transactions
- 🐳 **Docker Support**: Containerized app for easy deployment
- 📊 **Visualization**: Exploratory Data Analysis and dashboards

---

## 🗂️ Project Structure

credit_card_fraud_detection/
├── data/ # Dataset & SMOTE-balanced data
├── models/ # Trained model .pkl or .joblib files
├── kafka_producer.py # Kafka producer sending live transaction data
├── kafka_consumer.py # Fraud detection consumer
├── model_training.py # Model training and evaluation
├── email_alert.py # Sends alerts on fraud detection
├── Dockerfile # Containerization
├── requirements.txt # Project dependencies
└── README.md # You're here!

## Create a virtual environment and install dependencies
python -m venv venv310
venv310\Scripts\activate (Windows)
pip install -r requirements.txt

##  Train the model
python model_training.py

## Start real-time fraud detection
python kafka_producer.py
python kafka_consumer.py

## Email Alerting
Alerts are triggered when fraud is detected
## 📦 Requirements
pip install -r requirements.txt



