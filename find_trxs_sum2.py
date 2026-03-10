import pandas as pd
from itertools import combinations

# ---------------- INPUT PARAMETERS ----------------
csv_file = r"D:\Compare1\dwh_jan1.csv"
target_count = 60552
target_amount = 3297427905
output_file = r"D:\Compare1\matched_transactions.csv"

# number of top transactions to check
top_n = 160527
# --------------------------------------------------

print("Reading CSV file...")

# Read CSV
df = pd.read_csv(csv_file)

# Clean column names
df.columns = df.columns.str.strip()

# Ensure column names
df.columns = ["transaction_ref_id", "amount"]

# Convert amount to numeric
df["amount"] = pd.to_numeric(df["amount"], errors="coerce")

# Remove invalid rows
df = df.dropna()

# Sort by amount (largest first)
df = df.sort_values(by="amount", ascending=False)

# Take only top N rows for fast search
df_top = df.head(top_n)

print("Total rows in CSV:", len(df))
print("Searching top", len(df_top), "transactions")

transactions = list(zip(df_top["transaction_ref_id"], df_top["amount"]))

found = False
result = []

print("Searching combinations...")

for combo in combinations(transactions, target_count):

    total = sum(x[1] for x in combo)

    if total == target_amount:

        print("\nMATCH FOUND\n")

        for txn in combo:
            print(txn[0], txn[1])

            result.append({
                "transaction_ref_id": txn[0],
                "amount": txn[1]
            })

        found = True
        break

if found:

    result_df = pd.DataFrame(result)

    result_df.to_csv(output_file, index=False)

    print("\nOutput CSV created:")
    print(output_file)

else:

    print("No matching transactions found in top", top_n, "rows.")
