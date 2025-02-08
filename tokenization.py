import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
import os

# Ensure NLTK tokenizer is available
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

def load_text(file_path):
    """Load text from a file with error handling."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"❌ Error: File not found at {file_path}")

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read().strip()
    
    if not text:
        raise ValueError(f"⚠️ Warning: File at {file_path} is empty!")

    return text

def tokenize_and_chunk(text, chunk_size=256, overlap=50):
    """
    Tokenizes text into sentences and groups them into chunks.
    Maintains overlap between chunks for better context retention.
    """
    sentences = sent_tokenize(text)  # Sentence tokenization
    chunks = []
    current_chunk = []
    current_length = 0

    for i, sentence in enumerate(sentences):
        words = word_tokenize(sentence)  # Proper word tokenization
        sentence_length = len(words)

        # If adding this sentence exceeds chunk size, save current chunk
        if current_length + sentence_length > chunk_size:
            chunks.append(" ".join(current_chunk))  # Store current chunk
            
            # Ensure overlap is sentence-based, not just word-based
            if len(current_chunk) >= overlap:
                current_chunk = current_chunk[-overlap:]  # Retain only last `overlap` sentences
            else:
                current_chunk = []  # If too small, start fresh

            current_length = sum(len(word_tokenize(s)) for s in current_chunk)  # Reset length

        current_chunk.append(sentence)
        current_length += sentence_length

    if current_chunk:
        chunks.append(" ".join(current_chunk))  # Add last chunk

    # Filter out empty or very short chunks
    return [chunk for chunk in chunks if len(word_tokenize(chunk)) > 10]

def save_chunks(chunks, output_path):
    """Save tokenized and chunked text into a file (overwrite if exists)."""
    with open(output_path, "w", encoding="utf-8") as file:
        for chunk in chunks:
            file.write(chunk + "\n\n")  # Separate chunks with double newlines

if __name__ == "__main__":
    input_file = "K:/slm_project/data/preprocessed_text.txt"
    output_file = "K:/slm_project/data/tokenized_chunks.txt"

    print("📥 Loading preprocessed text...")
    try:
        text = load_text(input_file)

        print("🔍 Tokenizing and chunking text...")
        chunks = tokenize_and_chunk(text, chunk_size=256)

        print("💾 Saving tokenized chunks...")
        save_chunks(chunks, output_file)

        print(f"✅ Tokenized chunks saved to: {output_file}")
        print(f"📊 Total Chunks Created: {len(chunks)}")
        avg_size = sum(len(word_tokenize(chunk)) for chunk in chunks) / len(chunks)
        print(f"📏 Average Chunk Size: {avg_size:.2f} words")

        # Show a sample chunk for verification
        print("\n🔎 Sample Tokenized Chunks (First 3):")
        print("\n---\n".join(chunks[:3]) if len(chunks) >= 3 else "⚠️ Less than 3 chunks generated.")

    except (FileNotFoundError, ValueError) as e:
        print(e)
