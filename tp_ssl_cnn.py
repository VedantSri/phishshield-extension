import pandas as pd
import numpy as np
from gensim.models import Word2Vec
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from sklearn.model_selection import train_test_split
import random

print("🔥 Starting TP-SSL CNN")

# ======================
# Load data
# ======================
df = pd.read_csv("balanced_dataset.csv")
texts = df["text"].astype(str)

# ======================
# Transformations
# ======================
def transform(text):
    words = text.split()

    # Randomly choose transformation
    choice = random.randint(0, 2)

    if choice == 0:
        return text, 0  # original

    elif choice == 1:
        return " ".join(words[::-1]), 1  # reversed

    elif choice == 2:
         words_copy = words.copy()
    random.shuffle(words_copy[:len(words)//2])  # shuffle only half
    return " ".join(words_copy), 2 # shuffled


new_texts = []
labels = []

for t in texts:
    new_t, label = transform(t)
    new_texts.append(new_t)
    labels.append(label)

print("✅ Transformations applied")

# ======================
# Tokenize
# ======================
sentences = pd.Series(new_texts).apply(lambda x: x.split())

# ======================
# Word2Vec
# ======================
w2v = Word2Vec(sentences, vector_size=64, min_count=1)

# ======================
# Convert to matrix
# ======================
max_len = 50

def convert(sentences):
    data = []
    for sentence in sentences:
        vec = [w2v.wv[word] for word in sentence[:max_len] if word in w2v.wv]

        while len(vec) < max_len:
            vec.append(np.zeros(64))

        data.append(vec)

    return np.array(data)

X = convert(sentences)
X = X.reshape(len(X), max_len, 64, 1)
y = np.array(labels)

print("Shape:", X.shape)

# ======================
# Train-test split
# ======================
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ======================
# CNN Model
# ======================
model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(max_len, 64, 1)),
    MaxPooling2D((2,2)),
    Flatten(),
    Dense(64, activation='relu'),
    Dense(3, activation='softmax')  # 3 transformations
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

print("✅ Model built")

# ======================
# Train
# ======================
model.fit(
    X_train,
    y_train,
    epochs=6,
    batch_size=32,
    validation_data=(X_test, y_test)
)

# ======================
# Evaluate
# ======================
loss, acc = model.evaluate(X_test, y_test)

print("\n🔥 TP-SSL RESULTS")
print("Accuracy:", acc)
print("Loss:", loss)