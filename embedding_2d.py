import pandas as pd
from gensim.models import Word2Vec

print("🔥 Starting 2D Embedding")

# ✅ Load dataset
df = pd.read_csv("balanced_dataset.csv")

# ✅ Shuffle (important)
df = df.sample(frac=1).reset_index(drop=True)

# ✅ Use correct column
sentences = df["text"].astype(str).apply(lambda x: x.split())

print("✅ Data prepared")

# ✅ Train Word2Vec model
model = Word2Vec(
    sentences,
    vector_size=64,
    window=5,
    min_count=1,
    workers=4
)

print("✅ Word2Vec trained")

# ✅ Convert one sentence to vectors (example)
sample = sentences.iloc[0]

vectors = [model.wv[word] for word in sample if word in model.wv]

print("Sample word:", sample[0] if len(sample) > 0 else "N/A")
print("Vector shape:", len(vectors), "x", len(vectors[0]) if len(vectors) > 0 else 0)

print("✅ 2D Embedding done!")