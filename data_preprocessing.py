import pandas as pd

print("📥 Loading Enron dataset...")
enron = pd.read_csv("emails.csv")

# Extract body
def extract_body(text):
    if isinstance(text, str):
        parts = text.split("\n\n", 1)
        if len(parts) > 1:
            return parts[1].strip()
    return ""

enron["text"] = enron["message"].apply(extract_body)

# Remove empty
enron = enron[enron["text"].str.len() > 20]

# Label = 0 (normal emails)
enron["label"] = 0

enron = enron[["text", "label"]]

print("✅ Enron loaded:", len(enron))


print("📥 Loading Nazario dataset...")
nazario = pd.read_csv("nazario.csv")

# Adjust columns if needed
# (Check your column names if error comes)

nazario["text"] = nazario.iloc[:, 0]   # text column
nazario["label"] = 1                  # phishing

nazario = nazario[["text", "label"]]

print("✅ Nazario loaded:", len(nazario))


# 🔥 MERGE BOTH
final_df = pd.concat([enron, nazario], ignore_index=True)

# Shuffle dataset
final_df = final_df.sample(frac=1).reset_index(drop=True)

# Save
final_df.to_csv("final_dataset.csv", index=False)

print("🔥 FINAL DATASET CREATED:", len(final_df))

#BALANCE DATASET

phishing = final_df[final_df["label"] == 1]
ham = final_df[final_df["label"] == 0]

# Take equal number of ham samples
ham_sampled = ham.sample(n=len(phishing), random_state=42)

balanced_df = pd.concat([ham_sampled, phishing])
balanced_df = balanced_df.sample(frac=1).reset_index(drop=True)

balanced_df.to_csv("balanced_dataset.csv", index=False)

print(" BALANCED DATASET:", len(balanced_df))