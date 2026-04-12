import pandas as pd
import numpy as np
import tensorflow as tf
from gensim.models import Word2Vec
from tensorflow.keras.layers import Input, Dense, Flatten, Concatenate, Conv2D, MaxPooling2D, Embedding, GlobalAveragePooling1D
from tensorflow.keras.models import Model
from tensorflow.keras.layers import TextVectorization
from sklearn.model_selection import train_test_split

print("🔥 Starting Ensemble Model")

# ✅ Load dataset
df = pd.read_csv("balanced_dataset.csv")

# ✅ Shuffle dataset
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# ✅ Use correct column
texts = df["text"].astype(str)
labels = df["label"].values

# ======================
# Train-test split
# ======================
X_train_text, X_test_text, y_train, y_test = train_test_split(
    texts, labels, test_size=0.2, random_state=42
)

# ======================
# 1D (Transformer branch)
# ======================
vectorizer = TextVectorization(max_tokens=10000, output_sequence_length=100)
vectorizer.adapt(X_train_text)

X1_train = vectorizer(X_train_text)
X1_test = vectorizer(X_test_text)

input1 = Input(shape=(100,))
x1 = Embedding(10000, 64)(input1)
x1 = GlobalAveragePooling1D()(x1)

# ======================
# 2D (CNN branch)
# ======================
sentences_train = X_train_text.apply(lambda x: x.split())
sentences_test = X_test_text.apply(lambda x: x.split())

w2v = Word2Vec(sentences_train, vector_size=64, min_count=1)

max_len = 50

def convert(sentences):
    data = []
    for sentence in sentences:
        vec = [w2v.wv[word] for word in sentence[:max_len] if word in w2v.wv]
        while len(vec) < max_len:
            vec.append(np.zeros(64))
        data.append(vec)
    return np.array(data)

X2_train = convert(sentences_train).reshape(len(sentences_train), max_len, 64, 1)
X2_test = convert(sentences_test).reshape(len(sentences_test), max_len, 64, 1)

input2 = Input(shape=(max_len, 64, 1))
x2 = Conv2D(32, (3,3), activation='relu')(input2)
x2 = MaxPooling2D((2,2))(x2)
x2 = Flatten()(x2)

# ======================
# Combine
# ======================
combined = Concatenate()([x1, x2])

x = Dense(64, activation='relu')(combined)
output = Dense(1, activation='sigmoid')(x)

model = Model(inputs=[input1, input2], outputs=output)

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

print("✅ Ensemble Model Built")

# ======================
# Train
# ======================
model.fit(
    [X1_train, X2_train],
    y_train,
    epochs=3,
    batch_size=32,
    validation_data=([X1_test, X2_test], y_test)
)

# ======================
# Evaluate
# ======================
loss, acc = model.evaluate([X1_test, X2_test], y_test)

print("\n🔥 FINAL TEST RESULTS")
print("Test Accuracy:", acc)
print("Test Loss:", loss)