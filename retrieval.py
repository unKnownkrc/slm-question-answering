import os
import faiss
import torch
import numpy as np
import nltk
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer
import random
from elasticsearch import Elasticsearch

# Ensure NLTK sentence tokenizer is available
nltk.download("punkt")

# Paths
EMBEDDING_PATH = "K:/slm_project/data/embeddings.index"
DATA_PATH = "K:/slm_project/data/tokenized_chunks.txt"

# Elasticsearch settings
ES_HOST = "localhost"
ES_PORT = 9200
ES_SCHEME = "http"
INDEX_NAME = "my_index"

# Load the SBERT model for question encoding
print("📥 Loading SBERT model...")
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index
if not os.path.exists(EMBEDDING_PATH):
    raise FileNotFoundError(f"❌ FAISS index file not found: {EMBEDDING_PATH}")
print("📂 Loading FAISS index...")
index = faiss.read_index(EMBEDDING_PATH)

# Load text chunks
if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"❌ Text data file not found: {DATA_PATH}")

print("📂 Loading text chunks...")
with open(DATA_PATH, "r", encoding="utf-8") as file:
    text_chunks = [line.strip() for line in file.readlines() if line.strip()]

if len(text_chunks) == 0:
    raise ValueError("❌ No valid text chunks found!")

# Initialize the Elasticsearch client
es = Elasticsearch([{'host': ES_HOST, 'port': ES_PORT, 'scheme': ES_SCHEME}])

# Check the connection
if es.ping():
    print("🚀 Elasticsearch is connected!")
else:
    print("❌ Elasticsearch connection failed!")

def search_es(query, top_k=2):
    """Searches Elasticsearch for relevant text."""
    body = {"query": {"match": {"text": query}}}
    response = es.search(index=INDEX_NAME, body=body, size=top_k)
    return [(hit["_source"]["text"], hit["_score"]) for hit in response["hits"]["hits"]]

def generate_fallback_response(question):
    """Generate a fallback response when no relevant answer is found."""
    words = question.split()
    keywords = [word for word in words if word.lower() not in {"what", "who", "when", "where", "how", "is", "the", "does", "in", "of"}]
    templates = [
        f"While I couldn’t find a direct answer, the book offers insights on {' '.join(keywords)}.",
        f"Although no specific information is available, {' '.join(keywords)} are discussed throughout the book.",
        f"The book does not provide an exact match, but covers aspects related to {' '.join(keywords)}.",
        f"No direct answer, but the book explores topics connected to {' '.join(keywords)}.",
        f"Unfortunately, no exact match, but themes around {' '.join(keywords)} appear in the book."
    ]
    return random.choice(templates) if keywords else "No exact answer, but the book covers relevant themes."

def retrieve_best_sentence(query: str, top_k=5):
    """Retrieves the most relevant sentences using FAISS and Elasticsearch."""
    query_embedding = model.encode([query], convert_to_tensor=True).cpu().numpy()
    distances, top_chunk_indices = index.search(query_embedding, top_k)
    retrieved_sentences = []

    for idx in top_chunk_indices[0]:  
        if idx < len(text_chunks):
            chunk = text_chunks[idx]
            sentences = sent_tokenize(chunk)
            sentence_embeddings = model.encode(sentences, convert_to_tensor=True).cpu().numpy()
            similarities = np.dot(sentence_embeddings, query_embedding.T).flatten()
            
            # Get top 2 most relevant sentences
            best_sentence_indices = np.argsort(similarities)[-2:][::-1]  
            retrieved_sentences.extend([sentences[i] for i in best_sentence_indices])
    
    return retrieved_sentences if retrieved_sentences else ["❌ No relevant answer found!"]
