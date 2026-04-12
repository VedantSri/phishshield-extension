import pandas as pd
import tensorflow as tf
from tensorflow.keras.layers import TextVectorization, Embedding, Dense, GlobalAveragePooling1D
from tensorflow.keras.models import Sequential
from sklearn.model_selection import train_test_split

print("🔥 Starting Transformer model")

# ✅ Load dataset
df = pd.read_csv("balanced_dataset.csv")

# ✅ Shuffle dataset
df = df.sample(frac=1).reset_index(drop=True)

# ✅ Check label distribution
print("📊 Label Distribution:")
print(df["label"].value_counts())

# ✅ Extract data
texts = df["text"].astype(str)
labels = df["label"].values

# ✅ Train-test split (IMPORTANT)
X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.2, random_state=42
)

print("Train size:", len(X_train))
print("Test size:", len(X_test))

# ✅ Vectorization (fit only on training data)
vectorizer = TextVectorization(max_tokens=10000, output_sequence_length=100)
vectorizer.adapt(X_train)

# Convert text → vectors
X_train = vectorizer(X_train)
X_test = vectorizer(X_test)

print("Shape:", X_train.shape)

# ✅ Build model
model = Sequential([
    Embedding(input_dim=10000, output_dim=64),
    GlobalAveragePooling1D(),
    Dense(64, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

print("✅ Model built")

# ✅ Train model
model.fit(X_train, y_train, epochs=3, batch_size=32)

# ✅ Evaluate on test data (REAL accuracy)
loss, acc = model.evaluate(X_test, y_test)
print("Test Accuracy:", acc)

print("\n🔥 FINAL TEST RESULTS")
print("Test Accuracy:", acc)
print("Test Loss:", loss)