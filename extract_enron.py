import pandas as pd

print("📥 Loading Enron dataset...")

enron = pd.read_csv("emails.csv")

print(enron.head())
print("\nColumns:", enron.columns)