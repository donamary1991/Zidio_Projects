import pandas as pd

fraud_samples = []
nonfraud_samples = []

# Keep count
fraud_target = 5000
nonfraud_target = 95000
chunk_size = 50_000

print("Reading transaction data in chunks...")

for chunk in pd.read_csv("data/train_transaction.csv", chunksize=chunk_size):
    fraud_chunk = chunk[chunk['isFraud'] == 1]
    nonfraud_chunk = chunk[chunk['isFraud'] == 0]

    # Add fraud rows
    if len(fraud_samples) < fraud_target:
        fraud_needed = fraud_target - len(fraud_samples)
        fraud_samples.append(fraud_chunk.head(fraud_needed))

    # Add non-fraud rows
    if len(nonfraud_samples) < nonfraud_target:
        nonfraud_needed = nonfraud_target - len(nonfraud_samples)
        nonfraud_samples.append(nonfraud_chunk.sample(n=min(nonfraud_needed, len(nonfraud_chunk)), random_state=42))

    # Break early if enough samples are collected
    if len(fraud_samples) > 0 and len(nonfraud_samples) > 0:
        total_rows = sum(len(f) for f in fraud_samples) + sum(len(nf) for nf in nonfraud_samples)
        if total_rows >= 100_000:
            break

# Combine collected samples
df_fraud = pd.concat(fraud_samples)
df_nonfraud = pd.concat(nonfraud_samples)
sampled_df = pd.concat([df_fraud, df_nonfraud]).sample(frac=1, random_state=42).reset_index(drop=True)

# Save to disk
sampled_df.to_csv("data/sample_100k.csv", index=False)
print(f"Saved stratified 100K sample with {len(df_fraud)} frauds and {len(df_nonfraud)} non-frauds.")
