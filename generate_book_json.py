import json
import os

# Define data paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # src/retrieval/
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "../../data"))  # Points to data/

input_file = os.path.join(DATA_DIR, "tokenized_chunks.txt")
output_file = os.path.join(DATA_DIR, "book.json")

# ✅ Check if input file exists
if not os.path.exists(input_file):
    print(f"❌ ERROR: {input_file} not found! Cannot generate book.json.")
    exit(1)

# ✅ Read all passages WITHOUT removing duplicates
with open(input_file, "r", encoding="utf-8") as f:
    passages = [line.strip() for line in f if line.strip()]  # Keep all 958 lines

# ✅ Print passage count to debug
print(f"📥 DEBUG: Loaded {len(passages)} raw passages from tokenized_chunks.txt")

# ✅ Convert to structured JSON, assigning a unique ID to each passage (even if duplicate)
book_data = [{"id": idx, "text": passage} for idx, passage in enumerate(passages)]

# ✅ Save structured JSON
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(book_data, f, indent=4, ensure_ascii=False)

print(f"✅ Book JSON file created: {output_file} ({len(book_data)} passages)")
