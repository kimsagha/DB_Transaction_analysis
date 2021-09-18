import pandas as pd

fraud = pd.read_csv(r'Data/fraud', names=['credit_card_number', 'ipv4', 'state'])
fraud.drop([0], inplace=True)
print(fraud.head(10))
fraud.to_csv('Data/fraud_structured', index=False)
