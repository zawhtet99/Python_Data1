import pandas as pd

file1 = r"D:\Compare1\ap_jan1.csv"
file2 = r"D:\Compare1\dwh_jan1.csv"

df1 = pd.read_csv(file1, encoding="latin1", engine="python", on_bad_lines="skip")
df2 = pd.read_csv(file2, encoding="latin1", engine="python", on_bad_lines="skip")

print("File1 Columns:", df1.columns)
print("File2 Columns:", df2.columns)

# CHANGE THIS to your real column
key_column = df1.columns[0]

df1.set_index(key_column, inplace=True)
df2.set_index(key_column, inplace=True)

only_in_file1 = df1[~df1.index.isin(df2.index)]
only_in_file2 = df2[~df2.index.isin(df1.index)]

common_index = df1.index.intersection(df2.index)

changed_values = df1.loc[common_index].compare(df2.loc[common_index])

only_in_file1.to_csv("only_in_file1.csv")
only_in_file2.to_csv("only_in_file2.csv")
changed_values.to_csv("changed_values.csv")

print("CSV comparison completed.")
