import pandas as pd

# Load sampled data (100k)
print("Loading sampled transaction data...")
trans = pd.read_csv("data/sample_100k.csv")
identity = pd.read_csv("data/train_identity.csv")

# Merge transaction + identity on TransactionID
print("Merging transaction and identity data...")
df = trans.merge(identity, on="TransactionID", how="left")

# Basic preprocessing
df.fillna(-999, inplace=True)
df.drop(['TransactionID', 'TransactionDT'], axis=1, inplace=True, errors='ignore')

# Separate features and labels
y = df['isFraud']
X = df.drop('isFraud', axis=1)

# Optional: Drop string/object columns if any (to use directly with sklearn)
X = X.select_dtypes(include=['number'])

# Save processed files
X.to_csv("data/X_processed.csv", index=False)
y.to_csv("data/y_processed.csv", index=False)

print("✅ ETL complete and files saved.")
