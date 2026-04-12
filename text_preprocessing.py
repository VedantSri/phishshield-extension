print("File started")
import pandas as pd
import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

# Download once
nltk.download('stopwords', quiet=True)

# Load cleaned dataset
df = pd.read_csv("cleaned_nazario.csv")

# Initialize tools
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

def preprocess(text):
    # Lowercase
    text = text.lower()

    # Replace URLs
    text = re.sub(r'http\S+|www\S+', 'URL', text)

    # Remove emails
    text = re.sub(r'\S+@\S+', 'EMAIL', text)

    # Remove non-alphabet
    text = re.sub(r'[^a-z\s]', '', text)

    # Tokenize
    words = text.split()

    # Remove stopwords + stemming
    words = [stemmer.stem(word) for word in words if word not in stop_words]

    return " ".join(words)

# Apply preprocessing
df["processed_text"] = df["text"].apply(preprocess)

# Show sample
print(df[["text", "processed_text"]].head())

# Save
df.to_csv("processed_nazario.csv", index=False)

print("\n✅ Text preprocessing done!")