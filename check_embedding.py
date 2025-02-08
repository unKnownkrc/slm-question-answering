import faiss
import numpy as np

# Path to stored FAISS index
EMBEDDING_PATH = "K:/slm_project/data/embeddings.index"

# Load the FAISS index
print("📥 Loading FAISS index...")
index = faiss.read_index(EMBEDDING_PATH)

# Check number of stored embeddings
num_vectors = index.ntotal
print(f"✅ FAISS index contains {num_vectors} embeddings.")

# Retrieve the first 3 embeddings
print("🔍 Retrieving sample embeddings...")

# FAISS doesn't support direct retrieval for IndexFlatL2, so we use reconstruct_n
sample_size = min(3, num_vectors)  # Limit to available vectors
embeddings = np.array([index.reconstruct(i) for i in range(sample_size)])

# Print first 3 embeddings
print("\n📌 Sample Embeddings (First 3 rows):")
print(embeddings)
