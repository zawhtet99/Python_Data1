import pandas as pd

# -------- PARAMETERS --------
csv_file = r"D:\Compare1\dwh_jan1.csv"
target_count = 60552
target_amount = 3297427905
output_file = r"D:\Compare1\matched_transactions.csv"
# ----------------------------

print("Reading CSV...")

df = pd.read_csv(csv_file)

df.columns = df.columns.str.strip()
df.columns = ["transaction_ref_id", "amount"]

df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
df = df.dropna()

# convert to integer for faster comparison
df["amount"] = df["amount"].astype(int)

# sort largest first
df = df.sort_values("amount", ascending=False).reset_index(drop=True)

ids = df["transaction_ref_id"].tolist()
amounts = df["amount"].tolist()

n = len(amounts)

print("Total transactions:", n)

found = False
result = []

# -------- GREEDY SEARCH --------

for start in range(min(2000, n)):

    selected = []
    total = 0

    for i in range(start, n):

        if len(selected) < target_count and total + amounts[i] <= target_amount:
            selected.append((ids[i], amounts[i]))
            total += amounts[i]

        if len(selected) == target_count:

            if total == target_amount:
                result = selected
                found = True
                break
            else:
                break

    if found:
        break

# --------------------------------

if found:

    print("\nMATCH FOUND\n")

    for r in result:
        print(r[0], r[1])

    result_df = pd.DataFrame(result, columns=["transaction_ref_id", "amount"])
    result_df.to_csv(output_file, index=False)

    print("\nOutput CSV saved:")
    print(output_file)

else:
    print("No matching combination found.")
