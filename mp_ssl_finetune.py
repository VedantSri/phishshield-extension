import pandas as pd
import tensorflow as tf
from tensorflow.keras.layers import TextVectorization, Embedding, Dense, GlobalAveragePooling1D
from tensorflow.keras.models import Sequential
from sklearn.model_selection import train_test_split

print("🔥 MP-SSL Fine-Tuning Started")

# Load data
df = pd.read_csv("balanced_dataset.csv")

texts = df["text"].astype(str)
labels = df["label"].values

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.2, random_state=42
)

# Vectorization
vectorizer = TextVectorization(max_tokens=10000, output_sequence_length=100)
vectorizer.adapt(X_train)

X_train = vectorizer(X_train)
X_test = vectorizer(X_test)

# 🔥 SAME BASE AS MP-SSL (important)
model = Sequential([
    Embedding(input_dim=10000, output_dim=64),
    GlobalAveragePooling1D(),
    Dense(128, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

print("✅ Model ready for fine-tuning")

# Train
model.fit(
    X_train,
    y_train,
    epochs=3,
    batch_size=32,
    validation_data=(X_test, y_test)
)

# Evaluate
loss, acc = model.evaluate(X_test, y_test)

print("\n🔥 FINAL RESULTS AFTER SSL")
print("Test Accuracy:", acc)
print("Test Loss:", loss)