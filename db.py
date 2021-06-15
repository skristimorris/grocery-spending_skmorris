# db.py

import pandas as pd

db = "/Users/skm/Documents/MHCI/Summer 2021/HCI 584/Project/grocery-spending_skmorris/data/expenses.csv"

df = pd.read_csv(db)
print(df)

col_names = list(df)
print(col_names)