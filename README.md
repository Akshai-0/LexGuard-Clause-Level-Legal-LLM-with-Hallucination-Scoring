# Legal LLM Auditor

A pipeline for analyzing legal documents and detecting hallucinations in Large Language Model (LLM) generated insights.
This project explores how AI can assist in legal document auditing while also addressing one of the biggest problems with modern LLMs: **hallucinated claims that are not supported by the source text.**

---

## Problem
LLMs can generate convincing legal analysis, but they sometimes produce statements that are **not actually present in the document**.
In legal contexts, this can lead to misleading or incorrect conclusions.
This project introduces a verification layer that **audits LLM-generated insights against the original legal document** to identify unsupported claims and measure hallucination risk.

---

## Pipeline
Legal Document (PDF)  
→ Text Extraction  
→ Sentence Chunking  
→ Semantic Embeddings  
→ Clause Clustering (KMeans)  
→ LLM Legal Analysis  
→ Insight Generation based on User Intent  
→ Ironclad Audit (Claim Verification)  
→ Hallucination Score

---

## Key Features

• Extracts and processes legal documents from PDFs  
• Groups related clauses using semantic embeddings  
• Generates legal insights using an LLM  
• Verifies generated claims against the source document  
• Detects hallucinated or unsupported statements  
• Produces a hallucination risk score

---

## Tech Stack

Python  

Libraries:
- pdfplumber
- nltk
- scikit-learn
- sentence-transformers
- numpy
- openai (Groq API compatible)

Models:
- Sentence Transformers (all-MiniLM-L6-v2)
- LLaMA 3.3 70B via Groq

---

## Project Structure

legal-llm-auditor
│
├── main.py
├── sample_contract.pdf
├── example_output.json
├── requirements.txt
└── README.md

---

## Running the Project

Install dependencies:
pip install -r requirements.txt
Run the pipeline:
python main.py
You will be prompted to provide:
- a legal document (PDF)
- a query or investigation goal
The system will analyze the document, generate legal insights, run a hallucination audit, and save the results.

---

## Example Use Cases
- Contract risk analysis
- Legal document auditing
- AI compliance verification
- LLM hallucination evaluation

---

## Author

Akshai D K  
AI / Future Technology Projects
