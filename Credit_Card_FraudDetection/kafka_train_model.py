# model_training.py
import pandas as pd
from xgboost import XGBClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix, roc_auc_score
from imblearn.over_sampling import SMOTE
import joblib

# Load your processed dataset
X = pd.read_csv("data/X_processed.csv")
y = pd.read_csv("data/y_processed.csv").values.ravel()

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.2, random_state=42)

# Balance the dataset
sm = SMOTE(random_state=42)
X_res, y_res = sm.fit_resample(X_train, y_train)

# Train XGBoost
model = XGBClassifier(use_label_encoder=False, eval_metric="logloss")
model.fit(X_res, y_res)

# Save model
joblib.dump(model, "fraud_model.joblib")

# Save scaler if used (optional)
from sklearn.preprocessing import MinMaxScaler
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)
joblib.dump(scaler, "scaler.joblib")

# Evaluation
y_pred = model.predict(X_test)
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
print(f"ROC AUC: {roc_auc_score(y_test, model.predict_proba(X_test)[:,1]):.4f}")
