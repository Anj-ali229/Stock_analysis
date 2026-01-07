import pandas as pd
import sqlite3

df = pd.read_csv("infy.csv")
df['Date'] = pd.to_datetime(df['Date'], format='%d-%m-%Y')

conn = sqlite3.connect("stock_data.db")

df.to_sql("INFY_STOCK", conn, if_exists="replace", index=False)

conn.close()

print("successful")
