# ⚖️ Legal LLM Auditor

> An AI pipeline that analyzes legal documents and catches hallucinations in LLM-generated insights — before they cost you.

---

## The Problem

LLMs write convincing legal analysis. They also make things up.

In legal contexts, a fabricated clause or unsupported claim isn't just wrong — it's dangerous. **Legal LLM Auditor adds a verification layer** that audits every AI-generated insight against your source document and flags what can't be proven.

---

## Pipeline
```
PDF → Text Extraction → Sentence Chunking → Semantic Embeddings
    → Clause Clustering → LLM Analysis → Insight Generation
    → Ironclad Audit → Hallucination Score
```

---

## Features

- 📄 Extracts and processes legal documents from PDFs
- 🔗 Groups related clauses using semantic embeddings + KMeans
- 🤖 Generates legal insights via LLaMA 3.3 70B (Groq)
- 🔍 Verifies every claim against the source document
- 🚨 Flags hallucinated or unsupported statements
- 📊 Outputs a hallucination risk score

---

## Tech Stack

| Layer | Tools |
|---|---|
| Document Processing | `pdfplumber`, `nltk` |
| Embeddings & Clustering | `sentence-transformers`, `scikit-learn`, `numpy` |
| LLM | LLaMA 3.3 70B via Groq (`openai`-compatible) |
| Embedding Model | `all-MiniLM-L6-v2` |

---

## Quickstart
```bash
pip install -r requirements.txt
python main.py
```

You'll be prompted for a **PDF** and a **query or investigation goal**. The pipeline handles the rest and saves results to `example_output.json`.

---

## Use Cases

- Contract risk analysis
- Legal document auditing
- AI compliance verification
- LLM hallucination benchmarking

---

## Project Structure
```
legal-llm-auditor/
├── App.bat
├── sample_contract.pdf
├── Code.py
├── requirements.txt
└── README.md
```

---
## Author 
Akshai D K <br>
AI / Future Technology Projects
