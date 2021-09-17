import pandas as pd
import mysql.connector

mydb = mysql.connector.connect(
  host="localhost",
  user="kimiya.sagha@gmail.com",
  password="jihweh-wurryx-8Rutze"
)

print(mydb)

# df = pd.read_csv(r'fraud', names=['credit_card_number', 'ipv4', 'state'])
# df.drop([0], inplace=True)
# print(df.head(10))
