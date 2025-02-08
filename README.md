# **Devlancers Data Science Internship – Round 2 Task: SLM Question Answering System**

## 📌 **Project Overview**

This project implements a **Small Language Model (SLM) for Question Answering** using **hybrid search** (FAISS + Elasticsearch). The system retrieves relevant answers from a book based on user queries.

---

## 📂 **Project Structure**

```
slm_project/
│── data/                      # Contains book.json and tokenized text
│── src/
│   ├── preprocessing/         # Preprocessing scripts
│   │   ├── extract_text.py    # Extracts raw text from the book
│   │   ├── tokenize_text.py   # Tokenizes text into passages
│   │   ├── create_embeddings.py # Generates SBERT embeddings
│   ├── retrieval/             # Retrieval scripts
│   │   ├── generate_book_json.py # Converts text into JSON format
│   │   ├── index_passages.py  # Indexes passages in Elasticsearch
│   │   ├── retrieval.py       # Retrieves answers using FAISS + Elasticsearch
│   ├── main.py                # Main interactive Q&A system
│── README.md                  # Project documentation
│── requirements.txt            # Required dependencies
```

---

## 🚀 **Installation & Setup**

### **1️⃣ Create a Virtual Environment**

```sh
python -m venv slm_env
slm_env\Scripts\activate     # For Windows
```

### **2️⃣ Install Dependencies**

```sh
pip install -r requirements.txt
```

### **3️⃣ Start Elasticsearch** (Ensure it’s running before indexing data)

```sh
# Start Elasticsearch (Windows)
elasticsearch.bat
```

---

## ⚙️ **Running the Preprocessing Pipeline**

Before retrieving answers, preprocess the book using:

```sh
python src/preprocessing/extract_text.py
python src/preprocessing/tokenize_text.py
python src/preprocessing/create_embeddings.py
```

Then, generate the book JSON:

```sh
python src/retrieval/generate_book_json.py
```

And index passages into Elasticsearch:

```sh
python src/retrieval/index_passages.py
```

---

## 🔎 **Running the Question Answering System**

### **Interactive Mode (Continuous Q&A Loop)**

```sh
python main.py
```

* This allows you to enter multiple questions interactively.
* The system **keeps running** until you type  **`exit`** .

### **Command-Line Query Execution**

```sh
python main.py "Who is the author of this book?"
```

* This starts the Q&A system and lets you **continue asking** more questions.
* Type **`exit`** to end the session.

---

## 📊 **Observations & Learnings**

* **Hybrid search** improves accuracy by combining **semantic search (FAISS)** and  **keyword-based retrieval (Elasticsearch)** .
* **Tokenization and chunking** significantly impact retrieval performance.
* **Using SBERT embeddings** enhances passage relevance in dense retrieval.
* **Preprocessing is crucial** for effective indexing and retrieval.

---

## 🔗 **Repository & Submission**

Ensure all project files are uploaded to your GitHub repository manually.

---

## 🎯 **Final Deliverables**

✅ **Working Question Answering system**

✅ **Documented README.md with setup & usage details**

✅ **GitHub repository ready for submission**
