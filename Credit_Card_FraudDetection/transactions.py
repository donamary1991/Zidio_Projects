import pandas as pd
import random
import time
from datetime import datetime, timedelta

# Load processed feature and label datasets
X = pd.read_csv("data/X_processed.csv")
y = pd.read_csv("data/y_processed.csv").values.ravel()  # convert to 1D

# Add metadata columns
n = len(X)
X['transaction_id'] = [random.randint(1000, 9999) for _ in range(n)]
X['user_id'] = [random.randint(1, 100) for _ in range(n)]
X['location'] = [random.choice(['US', 'IN', 'CN', 'BR']) for _ in range(n)]

# Generate timestamps spaced 1 minute apart
base_time = datetime.now()
X['timestamp'] = [base_time - timedelta(minutes=i) for i in range(n)]

# Append label column
X['is_fraud'] = y

# Reorder columns (optional)
cols = ['transaction_id', 'user_id', 'amount'] if 'amount' in X.columns else []
cols += ['location', 'timestamp', 'is_fraud']
other_features = [c for c in X.columns if c not in cols]
X = X[cols[:3] + other_features + cols[3:]]

# Save to CSV
X.to_csv("data/transactions.csv", index=False)

print("✅ transactions.csv created successfully.")
