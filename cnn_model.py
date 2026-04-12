import numpy as np
import pandas as pd
from gensim.models import Word2Vec
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from sklearn.model_selection import train_test_split

print(" Starting CNN model")

# Load dataset
df = pd.read_csv("balanced_dataset.csv")

#  Shuffle dataset
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

#  Use correct column
sentences = df["text"].astype(str).apply(lambda x: x.split())

# Labels
y = df["label"].values

print(" Data prepared")

#  Train Word2Vec
w2v_model = Word2Vec(sentences, vector_size=64, window=5, min_count=1)

print(" Word2Vec trained")

#  Convert sentences → fixed-size matrices
max_len = 50
X = []

for sentence in sentences:
    vec = [w2v_model.wv[word] for word in sentence[:max_len] if word in w2v_model.wv]

    # Padding
    while len(vec) < max_len:
        vec.append(np.zeros(64))

    X.append(vec)

X = np.array(X)
X = X.reshape(X.shape[0], max_len, 64, 1)

print("Shape:", X.shape)

#  Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print("Train size:", len(X_train))
print("Test size:", len(X_test))

#  Build CNN
cnn = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(max_len, 64, 1)),
    MaxPooling2D((2,2)),
    Flatten(),
    Dense(64, activation='relu'),
    Dense(1, activation='sigmoid')
])

cnn.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

print(" Model built")

#  Train
cnn.fit(
    X_train,
    y_train,
    epochs=5,
    batch_size=32,
    validation_data=(X_test, y_test)
)

#  Evaluate
loss, acc = cnn.evaluate(X_test, y_test)

print("\n FINAL TEST RESULTS")
print("Test Accuracy:", acc)
print("Test Loss:", loss)