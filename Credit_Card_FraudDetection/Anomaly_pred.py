import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score, f1_score, precision_recall_curve, auc
from sklearn.ensemble import IsolationForest
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense
import tensorflow as tf

# Load data
X = pd.read_csv("data/X_processed.csv").values
y = pd.read_csv("data/y_processed.csv").values.ravel()

# Normalize features
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

# Separate normal data for training AE
X_train_ae = X_scaled[y == 0]
X_test = X_scaled
y_test = y

# === AUTOENCODER ===
input_dim = X.shape[1]
input_layer = Input(shape=(input_dim,))
encoded = Dense(32, activation='relu')(input_layer)
encoded = Dense(16, activation='relu')(encoded)
decoded = Dense(32, activation='relu')(encoded)
output_layer = Dense(input_dim, activation='sigmoid')(decoded)

autoencoder = Model(inputs=input_layer, outputs=output_layer)
autoencoder.compile(optimizer='adam', loss='mse')

# Train Autoencoder
autoencoder.fit(X_train_ae, X_train_ae, epochs=10, batch_size=256, shuffle=True, validation_split=0.1)

# Get reconstruction error (MSE) for test data
X_pred = autoencoder.predict(X_test)
ae_scores = np.mean(np.square(X_test - X_pred), axis=1)

# === ISOLATION FOREST ===
iso_forest = IsolationForest(contamination=0.025, random_state=42)
iso_forest.fit(X_train_ae)
if_scores = -iso_forest.decision_function(X_test)  # Flip sign to make it an anomaly score

# === SCORE NORMALIZATION ===
ae_scores = (ae_scores - ae_scores.min()) / (ae_scores.max() - ae_scores.min())
if_scores = (if_scores - if_scores.min()) / (if_scores.max() - if_scores.min())

# === SOFT ENSEMBLE ===
alpha = 0.5  # weight for AE
ensemble_scores = alpha * ae_scores + (1 - alpha) * if_scores

# === THRESHOLD TUNING ===
best_threshold = 0
best_f1 = 0
thresholds = np.linspace(0, 1, 200)

for threshold in thresholds:
    y_pred = (ensemble_scores > threshold).astype(int)
    f1 = f1_score(y_test, y_pred)
    if f1 > best_f1:
        best_f1 = f1
        best_threshold = threshold

# Final predictions
y_pred_final = (ensemble_scores > best_threshold).astype(int)

# === EVALUATION ===
print(f"\nBest Threshold: {best_threshold:.4f}, Best F1-Score: {best_f1:.4f}\n")

print("=== Ensemble Confusion Matrix ===")
print(confusion_matrix(y_test, y_pred_final))

print("\n=== Ensemble Classification Report ===")
print(classification_report(y_test, y_pred_final))

roc_auc = roc_auc_score(y_test, ensemble_scores)
precision, recall, _ = precision_recall_curve(y_test, ensemble_scores)
pr_auc = auc(recall, precision)

print(f"ROC-AUC (Ensemble): {roc_auc}")
print(f"Precision-Recall AUC: {pr_auc}")
