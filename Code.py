import pdfplumber
import numpy as np
from sklearn.cluster import KMeans
import nltk
nltk.download('punkt')
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer
from openai import OpenAI 
import time

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
MODEL_ID = "llama-3.3-70b-versatile"

client = OpenAI(
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

def read_pdf(file_path):
    text = ''                                     
    with pdfplumber.open(file_path) as pdf:         
        for page in pdf.pages:                     
            content = page.extract_text()
            if content:
                text += content + '\n'
    return text

def chunk_text(text):
    healed_text = " ".join(text.split())
    final_chunks = sent_tokenize(healed_text)
    return final_chunks

def embed_chunks(chunks):
    if not chunks:
        return np.array([])
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = np.array(model.encode(chunks))
    return embeddings

def cluster_chunks(chunks, embeddings):
    if len(embeddings) == 0:
        return []
    
    num_clusters = min(5, len(embeddings))
    if num_clusters < 1:
        return []
        
    kmeans = KMeans(n_clusters=num_clusters, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(embeddings)
    
    grouped_chunks = [[] for _ in range(num_clusters)]
    for i, cluster_id in enumerate(clusters):
        grouped_chunks[cluster_id].append(chunks[i])
        
    return grouped_chunks


def analyze_legal_categories(clustered_groups):
    results = []
    for i, group in enumerate(clustered_groups):
        context = "\n".join(group)
        prompt = f"Role: Legal Auditor. Summarize obligations and identify creative risks for this text:\n\n{context}"

        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=[{"role": "user", "content": prompt}]
        )
        analysis_text = response.choices[0].message.content
        
        results.append({
            "id": i,
            "original_text": context,
            "analysis": analysis_text
        })
    return results

def generate_legal_insights(labeled_paragraphs, user_query):
   
    final_reports = []
    for label, text in labeled_paragraphs.items():
        prompt = f"""
        ROLE: Senior Legal Auditor | CATEGORY: {label}
        USER INTENT: {user_query}
        CONTEXT: {text}
    
        TASK:
        1. Link this category to the user's intent.
        2. Find 1 non-obvious loophole.
        3. Flag high-severity items.
        """
        
        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=[{"role": "user", "content": prompt}]
        )
        analysis_text = response.choices[0].message.content
        
        final_reports.append({
            "category": label,
            "analysis": analysis_text,
            "source": text
        })
        
    return final_reports

def ironclad_audit(analysis, source_text):
    prompt = f"""
SOURCE TEXT:
{source_text}

ANALYSIS TO AUDIT:
{analysis}

TASK:
1. Extract ONLY factual claims present in the ANALYSIS.
2. For each claim, locate the EXACT supporting sentence in the SOURCE TEXT.
3. If an EXACT supporting sentence exists, quote it as Evidence.
4. If a RELATED statement exists but does not fully support the claim, quote the closest sentence as Evidence and classify the claim as partially existing.
5. If no relevant statement exists anywhere in the SOURCE TEXT, mark Evidence as 'NONE FOUND'.

RULES:
- Extract the MINIMUM number of factual claims necessary.
- Each claim must be directly verifiable from the SOURCE TEXT.
- If the SOURCE TEXT does not support the claim, it must be classified accordingly.


CLAIM CLASSIFICATION DEFINITIONS:
Claim-existing one's (Strictly No Hallucinations):
Claims fully supported by an exact sentence in SOURCE TEXT.

Claim-partially existing one's (Slight Hallucinations):
Claims where a related statement exists in the SOURCE TEXT but it does not fully support the claim.

Claim-not existing one's:
Claims where no relevant statement exists anywhere in the SOURCE TEXT.

FINAL OUTPUT FORMAT:

Claim-existing one's (Strictly No Hallucinations):
- Claim: [The Statement]
- Evidence: [Exact Quote]
- Verification: Pass/Fail

Claim-partially existing one's (Slight Hallucinations):
- Claim: [The Statement]
- Evidence: [Quote or 'NONE FOUND']
- Verification: Pass/Fail

Claim-not existing one's :
- Claim: [The Statement]
- Evidence: NONE FOUND
- Verification: Fail

FINAL HALLUCINATION AND RISK SCORES:
- Total Claims: Count of Existing + Count of Partial + Count of Not Existing
- Hallucination Score Calculation: ((0.5 * Count of Partial) + (1.0 * Count of Not Existing)) / Total Claims
- Final Hallucination Score: [Result as a percentage]
"""
    
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    print("PDF Clustering Tool (Groq Powered)")
    pdf_path = input("Enter PDF path: ").strip()
    user_query = input("Enter your search intent or query: ").strip()
    
    if pdf_path:
        try:
            print("[Step 1/6] Reading PDF...")
            text = read_pdf(pdf_path)
            print("Done.\n")
            
            print("[Step 2/6] Chunking text...")
            chunks = chunk_text(text)
            print(f"Total chunks: {len(chunks)} - Done.\n")
            
            if len(chunks) == 0:
                print("No text found in PDF.")
            else:
                print("[Step 3/6] Embedding chunks...")
                embeddings = embed_chunks(chunks)
                print("Done.\n")
                
                print("[Step 4/6] Clustering chunks...")
                groups = cluster_chunks(chunks, embeddings)
                print(f"Clustering complete. Formed {len(groups)} distinct topic groups.\n")
                
                print("[Step 5/6] Analyzing legal categories...")
                analyses = analyze_legal_categories(groups)
                print("Legal categories analyzed successfully.\n")
                
                print("[Step 6/6] Generating legal insights based on user intent...")
                labeled_paragraphs = {}
                for r in analyses:
                    labeled_paragraphs[f"Cluster {r['id']}"] = r['original_text']
                
                insights = generate_legal_insights(labeled_paragraphs, user_query)
                print("Insights generated successfully.\n")
                
                print("="*60)
                print("FINAL LEGAL INSIGHTS".center(60))
                print("="*60)
                for rep in insights:
                    print(f"[*] Category: {rep['category']}")
                    print(f"{rep['analysis']}\n")
                print("="*60)
                
                try:
                    print("\n[Step 7] Running Ironclad audit...")
                    audit_output = ironclad_audit(insights, text)
                    print("Ironclad audit complete.\n")
                    
                    print("="*60)
                    print("IRONCLAD VERIFICATION REPORT".center(60))
                    print("="*60)
                    print(audit_output)
                    print("="*60)
                    
                    
                except Exception as e:
                    print(f"Error running Ironclad audit: {e}")
                    
        except Exception as e:
            print(f"An error occurred: {e}")
    else:
        print("Please provide a valid PDF path.")
