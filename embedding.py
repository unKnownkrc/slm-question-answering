import os
import faiss
import torch
from sentence_transformers import SentenceTransformer

# Define paths
DATA_PATH = "K:/slm_project/data/tokenized_chunks.txt"
EMBEDDING_PATH = "K:/slm_project/data/embeddings.index"

# Load the SBERT model (this will convert text into meaningful numerical representations)
print("📥 Loading SBERT model for embeddings...")
model = SentenceTransformer("all-MiniLM-L6-v2")  # Lightweight and fast!

# Load tokenized text chunks
print("📂 Loading tokenized chunks...")
with open(DATA_PATH, "r", encoding="utf-8") as file:
    text_chunks = file.readlines()

# Convert text chunks into embeddings
print("🔍 Generating embeddings for text chunks...")
embeddings = model.encode(text_chunks, convert_to_tensor=True)

# Convert embeddings to a NumPy array for FAISS
embeddings = embeddings.cpu().numpy()

# Create FAISS index for efficient similarity search
print("⚡ Initializing FAISS index...")
dimension = embeddings.shape[1]  # Get the embedding vector size
index = faiss.IndexFlatL2(dimension)  # L2 (Euclidean) distance for similarity search
index.add(embeddings)

# Save FAISS index to disk
print("💾 Saving FAISS index for future use...")
faiss.write_index(index, EMBEDDING_PATH)

print(f"✅ Embeddings stored successfully in {EMBEDDING_PATH}")
