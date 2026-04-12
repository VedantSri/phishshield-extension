import pandas as pd
import tensorflow as tf
import numpy as np
from tensorflow.keras.layers import TextVectorization, Embedding, Dense
from tensorflow.keras.models import Sequential

print("🔥 Starting MP-SSL Transformer")

# Load data
df = pd.read_csv("balanced_dataset.csv")
texts = df["text"].astype(str)

# Shuffle
texts = texts.sample(frac=1, random_state=42).reset_index(drop=True)

# Vectorization
vectorizer = TextVectorization(max_tokens=10000, output_sequence_length=100)
vectorizer.adapt(texts)

X = vectorizer(texts)

# 🔥 MASKING FUNCTION
def mask_data(X, mask_token=0, mask_ratio=0.15):
    X_masked = X.numpy().copy()
    y = X.numpy().copy()

    for i in range(X_masked.shape[0]):
        for j in range(X_masked.shape[1]):
            if np.random.rand() < mask_ratio:
                X_masked[i][j] = mask_token

    return X_masked, y

print("⏳ Applying masking...")
X_masked, y = mask_data(X)

# ✅ FIXED MODEL
model = Sequential([
    Embedding(input_dim=10000, output_dim=64),
    Dense(128, activation='relu'),
    Dense(10000, activation='softmax')  # vocab size output
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

print("✅ Model built")

# Train
model.fit(X_masked, y, epochs=3, batch_size=32)

print("🔥 MP-SSL Training Done!")