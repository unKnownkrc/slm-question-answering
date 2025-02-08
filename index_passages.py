from elasticsearch import Elasticsearch
import json
from sentence_transformers import SentenceTransformer
import os

# Connect to Elasticsearch
es = Elasticsearch("http://localhost:9200")

# Load passages from book.json
book_path = r"K:\slm_project\data\book.json"
if not os.path.exists(book_path):
    raise FileNotFoundError(f"❌ File not found: {book_path}")

with open(book_path, "r", encoding="utf-8") as f:
    book_data = json.load(f)

# Ensure the data is a list of dictionaries
if not isinstance(book_data, list):
    raise ValueError("❌ Expected JSON to be a list of dictionaries!")

# Extract passages (only text fields)
passages = [entry["text"] for entry in book_data if "text" in entry]

if not passages:
    raise ValueError("❌ No valid passages found in book.json!")

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

def index_passages():
    index_name = "slm_index"

    # Create index with mapping if it doesn’t exist (Fixing deprecated `exists()` usage)
    if not es.indices.exists(index=index_name, allow_no_indices=True):
        es.indices.create(index=index_name, body={
            "mappings": {
                "properties": {
                    "text": {"type": "text"},
                    "embedding": {"type": "dense_vector", "dims": 384}  # Adjust for model
                }
            }
        })

    for i, passage in enumerate(passages):
        embedding = model.encode(passage).tolist()
        
        doc = {
            "text": passage,
            "embedding": embedding
        }
        es.index(index=index_name, id=i, document=doc)
    
    print(f"✅ Indexed {len(passages)} passages into Elasticsearch.")

# Run indexing
index_passages()
print(f"📦 Total passages loaded: {len(passages)}")
