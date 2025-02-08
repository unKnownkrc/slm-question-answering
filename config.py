import os

# === PATH CONFIGURATION ===
BASE_DIR = os.path.abspath(os.path.dirname(__file__))  # Base directory (src folder)
DATA_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "data"))  # Data folder
MODEL_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "models"))  # Model folder

BOOK_PATH = os.path.join(DATA_DIR, "india2020.pdf")  # Path to the book file
MODEL_PATH = os.path.join(MODEL_DIR, "slm_model.pth")  # Model save path

# === EMBEDDING CONFIGURATION ===
EMBEDDING_DIM = 768  # Dimension of word embeddings (e.g., BERT)
MAX_TOKENS = 512  # Maximum tokens per input (truncate if longer)

# === TRAINING HYPERPARAMETERS ===
BATCH_SIZE = 16  # Batch size for training
EPOCHS = 5  # Number of epochs for training
LEARNING_RATE = 3e-5  # Learning rate

# === RETRIEVAL SETTINGS ===
TOP_K = 5  # Number of top retrieved passages for QA

# === TOKENIZATION CONFIGURATION ===
TOKENIZER_MODEL = "bert-base-uncased"  # Model name for tokenizer

# === DEBUG SETTINGS ===
DEBUG_MODE = True  # Set to False to disable debug prints

# Print verification only if executed directly
if __name__ == "__main__" or DEBUG_MODE:
    print(f"Config Loaded:\n- Book Path: {BOOK_PATH}\n- Model Path: {MODEL_PATH}")
