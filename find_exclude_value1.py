import pandas as pd
from itertools import combinations

# CSV file path
file_path = r"D:\Compare1\dwh_jan1.csv"

# Required final amount after exclusion
required_amount = 700

# Read CSV
df = pd.read_csv(file_path)

# Ensure correct column names
df.columns = ["txn_id", "amount"]

# Calculate total
total_amount = df["amount"].sum()

print("Total Amount:", total_amount)

# Amount that must be excluded
exclude_amount = total_amount - required_amount

print("Amount to exclude:", exclude_amount)

transactions = list(zip(df["txn_id"], df["amount"]))

found = False

# Try combinations of transactions
for r in range(1, len(transactions) + 1):
    for combo in combinations(transactions, r):

        combo_sum = sum(x[1] for x in combo)

        if combo_sum == exclude_amount:

            print("\nTransactions to EXCLUDE:\n")

            for txn in combo:
                print(txn[0], txn[1])

            print("\nTotal Excluded:", combo_sum)

            found = True
            break

    if found:
        break

if not found:
    print("No combination found to match required amount.")
