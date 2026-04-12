print("🚀 Starting 1D Embedding")

import pandas as pd
import tensorflow as tf
from tensorflow.keras.layers import TextVectorization

print("✅ Libraries loaded")

# ✅ Load new dataset
df = pd.read_csv("balanced_dataset.csv")
print("✅ Data loaded")

# ✅ Shuffle (important)
df = df.sample(frac=1).reset_index(drop=True)

# ✅ Use correct column
texts = df["text"].astype(str)

# ✅ Vectorization
vectorizer = TextVectorization(
    max_tokens=10000,
    output_sequence_length=100
)

print("⏳ Adapting vectorizer...")
vectorizer.adapt(texts)

print("⏳ Converting text...")
X = vectorizer(texts)

print("Shape:", X.shape)

print("✅ 1D Embedding done!")