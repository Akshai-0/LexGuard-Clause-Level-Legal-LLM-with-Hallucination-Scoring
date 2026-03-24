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

## API Key Requirement

This project uses the Groq API for running LLM analysis.

To use the application, you will need your own Groq API key.

1. Get an API key from:
https://console.groq.com

2. When launching the web interface, the application will prompt you to enter your Groq API key.

The key is used only for the current session to run the LLM analysis pipeline.

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
├── Code.py
├── Readme.md
├── Sample Contract.pdf
├── index.html
└── requirements
```

---
## Author 
Akshai D K <br>
AI / Future Technology Projects
