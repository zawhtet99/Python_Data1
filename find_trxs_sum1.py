import pandas as pd
from itertools import combinations

# -------- INPUT PARAMETERS --------
csv_file = r"D:\Compare1\dwh_jan1.csv"
target_count = 60552
target_amount = 3297427905
output_file = r"D:\Compare1\matched_transactions.csv"
# ----------------------------------

print("Reading CSV file...")

# Read CSV
df = pd.read_csv(csv_file)

# Clean column names
df.columns = df.columns.str.strip()

# Ensure proper column names
df.columns = ["transaction_ref_id", "amount"]

# Convert amount to numeric
df["amount"] = pd.to_numeric(df["amount"])

# Convert dataframe to list
transactions = list(zip(df["transaction_ref_id"], df["amount"]))

print("Total transactions in file:", len(transactions))
print("Searching for transactions with:")
print("Count =", target_count)
print("Total Amount =", target_amount)
print()

found = False
result_rows = []

# Generate combinations for required transaction count
for combo in combinations(transactions, target_count):

    combo_sum = sum(x[1] for x in combo)

    if combo_sum == target_amount:

        print("MATCH FOUND\n")

        for txn in combo:
            print("Transaction:", txn[0], " Amount:", txn[1])

            result_rows.append({
                "transaction_ref_id": txn[0],
                "amount": txn[1]
            })

        print("\nTotal Transactions:", len(combo))
        print("Total Amount:", combo_sum)

        found = True
        break

if not found:
    print("No matching transaction set found.")
else:

    # Export result to CSV
    result_df = pd.DataFrame(result_rows)

    result_df.to_csv(output_file, index=False)

    print("\nOutput file created:")
    print(output_file)
