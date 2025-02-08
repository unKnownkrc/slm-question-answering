import re
import unicodedata
import nltk
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# Ensure correct NLTK data path
nltk.data.path.append("C:/Users/kravi/AppData/Roaming/nltk_data")
from nltk.tokenize import sent_tokenize

# Ensure necessary NLTK resources are available
nltk_resources = ["punkt", "wordnet"]
for resource in nltk_resources:
    try:
        nltk.data.find(f"tokenizers/{resource}")
    except LookupError:
        nltk.download(resource)

# Precompile regex patterns for efficiency
RE_EXTRA_SPACES = re.compile(r"\s+")
RE_FIX_JOINED_WORDS = re.compile(r"(\d*)([a-z]+)([A-Z])")  # Fix words stuck together
RE_CLEAN_TEXT = re.compile(r"[^a-zA-Z0-9.,!?'\-\s\"]")  # Keep punctuation & essential characters


def normalize_text(text):
    """Normalize Unicode text."""
    return unicodedata.normalize("NFKC", text)


def clean_text(text, lowercase=False):
    """Clean and structure the text while preserving meaning and readability."""
    text = normalize_text(text)
    text = RE_FIX_JOINED_WORDS.sub(r"\1-\2\3", text)  # Fix joined words like "tenyearold" → "ten-year-old"
    text = RE_CLEAN_TEXT.sub("", text)  # Remove unwanted special characters
    text = RE_EXTRA_SPACES.sub(" ", text).strip()  # Remove extra spaces
    if lowercase:
        text = text.lower()
    return text


def preprocess_text(text, lowercase=False):
    """Preprocess text while maintaining sentence structure and punctuation."""
    if not text.strip():  # Skip empty input
        return ""

    text = clean_text(text, lowercase)

    # Tokenize sentences to maintain structure
    sentences = sent_tokenize(text)
    processed_sentences = []

    for sent in sentences:
        sent = sent.strip()
        if sent:
            # Capitalize first letter of each sentence if needed
            sent = sent[0].upper() + sent[1:] if sent and sent[0].islower() else sent
            sent = re.sub(r'(?<=\?)\s*([A-Z])', lambda m: m.group(1).lower(), sent)  # Fix: '"?" He' → '"?" he'
            processed_sentences.append(sent)

    return " ".join(processed_sentences)  # Join sentences with proper spacing


def full_preprocessing_pipeline(text, lowercase=False):
    """Complete text preprocessing pipeline."""
    if not text.strip():  # Handle empty input early
        return ""
    return preprocess_text(text, lowercase)


if __name__ == "__main__":
    BASE_DIR = os.path.abspath("K:/slm_project/data/")
    input_file = os.path.join(BASE_DIR, "extracted_text_cleaned.txt")
    output_file = os.path.join(BASE_DIR, "preprocessed_text.txt")

    if not os.path.exists(input_file):
        logging.error(f"Input file not found at {input_file}")
    else:
        logging.info(f"Processing text from {input_file}")
        with open(input_file, "r", encoding="utf-8") as infile, open(output_file, "w", encoding="utf-8") as outfile:
            for line in infile:
                processed_line = full_preprocessing_pipeline(line, lowercase=True)  # Set lowercase=True if needed
                outfile.write(processed_line + "\n")

        logging.info(f"✅ Preprocessed text saved to: {output_file}")

        # Print sample output
        with open(output_file, "r", encoding="utf-8") as file:
            processed_text = file.read()

        logging.info("🔍 Sample Preprocessed Text (First 500 characters):")
        print(processed_text[:500])
