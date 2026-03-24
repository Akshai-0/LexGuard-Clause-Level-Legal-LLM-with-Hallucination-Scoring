import streamlit as st
import tempfile
import os
import sys

# Ensure the current directory is in the path so we can import Test1
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from Test1 import (
    read_pdf, 
    chunk_text, 
    embed_chunks, 
    cluster_chunks, 
    analyze_legal_categories, 
    generate_legal_insights, 
    ironclad_audit
)

# Page Configuration
st.set_page_config(page_title="AI Legal Auditor", page_icon="⚖️", layout="wide")

# Custom CSS for the Black and Cool Blue Theme
st.markdown("""
<style>
    /* Global Font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* Gradient Headers */
    h1, h2, h3 {
        background: -webkit-linear-gradient(45deg, #00e5ff, #0077ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800 !important;
    }

    /* Neon Buttons */
    .stButton>button {
        background: linear-gradient(90deg, #0055ff 0%, #00e5ff 100%);
        color: #ffffff !important;
        font-weight: 600;
        border: none;
        box-shadow: 0 4px 15px rgba(0, 229, 255, 0.3);
        border-radius: 8px;
        transition: all 0.3s ease;
        padding: 0.5rem 2rem;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0, 229, 255, 0.5);
    }

    /* Cards and Expanders */
    .streamlit-expanderHeader {
        background-color: #0b1120 !important;
        color: #00e5ff !important;
        border-radius: 6px;
        font-weight: 600;
        border: 1px solid #1a2b4c;
    }
    
    .streamlit-expanderContent {
        background-color: #050505 !important;
        border: 1px solid #1a2b4c;
        border-top: none;
        border-radius: 0 0 6px 6px;
    }

    /* Alerts / Callouts */
    .stAlert {
        background-color: #0a1329 !important;
        border: 1px solid #0055ff !important;
        color: #e2e8f0 !important;
        box-shadow: 0 0 10px rgba(0, 85, 255, 0.1);
    }

    /* Inputs */
    .stTextInput>div>div>input {
        background-color: #0b1120 !important;
        color: #00e5ff !important;
        border: 1px solid #1a2b4c !important;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div > div {
        background: linear-gradient(90deg, #0055ff 0%, #00e5ff 100%);
        box-shadow: 0 0 10px rgba(0, 229, 255, 0.5);
    }
</style>
""", unsafe_allow_html=True)


# --- Layout ---
st.title("⚖️ AI Legal Auditor")
st.markdown("<p style='color:#64748b; font-size: 1.1rem;'>Upload legal documents and extract deep insights powered by GenAI & Semantic Clustering.</p>", unsafe_allow_html=True)

st.sidebar.image("https://cdn-icons-png.flaticon.com/512/6037/6037084.png", width=60)
st.sidebar.header("Configuration")
st.sidebar.markdown("Configure your analysis settings here.")

uploaded_file = st.sidebar.file_uploader("Upload PDF Document", type=["pdf"])
user_query = st.sidebar.text_input("Search Intent / Query", placeholder="e.g., What are the main liabilities?")

if st.sidebar.button("Run Analysis", use_container_width=True):
    if not uploaded_file:
        st.sidebar.error("Please upload a PDF file first.")
    elif not user_query:
        st.sidebar.error("Please enter a search intent or query.")
    else:
        # Create a placeholder for temporary file writing
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            tmp_pdf_path = tmp_file.name

        try:
            st.markdown("### ⚙️ Analysis Pipeline")
            progress_bar = st.progress(0)
            status_text = st.empty()

            status_text.markdown("**[Step 1/7]** Reading PDF content...")
            text = read_pdf(tmp_pdf_path)
            progress_bar.progress(14)

            status_text.markdown("**[Step 2/7]** Chunking text into processable segments...")
            chunks = chunk_text(text)
            progress_bar.progress(28)

            if len(chunks) == 0:
                st.warning("No valid text found in the uploaded PDF.")
                progress_bar.progress(100)
            else:
                status_text.markdown(f"**[Step 3/7]** Embedding {len(chunks)} chunks...")
                embeddings = embed_chunks(chunks)
                progress_bar.progress(42)

                status_text.markdown("**[Step 4/7]** Clustering data by semantic similarity...")
                groups = cluster_chunks(chunks, embeddings)
                progress_bar.progress(57)

                status_text.markdown(f"**[Step 5/7]** Analyzing {len(groups)} distinct legal categories...")
                analyses = analyze_legal_categories(groups)
                progress_bar.progress(71)

                status_text.markdown("**[Step 6/7]** Synthesizing legal insights based on user intent...")
                labeled_paragraphs = {f"Category Cluster {r['id']}": r['original_text'] for r in analyses}
                insights = generate_legal_insights(labeled_paragraphs, user_query)
                progress_bar.progress(85)

                status_text.markdown("**[Step 7/7]** Performing Ironclad Fact-check Audit...")
                audit_output = ironclad_audit(insights, text)
                progress_bar.progress(100)
                
                status_text.success("Analysis Complete! Scroll down to view the results.")

                st.markdown("<br/>", unsafe_allow_html=True)
                
                # --- Result Presentation ---
                col1, col2 = st.columns([1, 1], gap="large")
                
                with col1:
                    st.header("🔍 Legal Insights")
                    st.markdown("AI-driven synthesis linking legal clauses to your targeted intent.")
                    if isinstance(insights, list):
                        for rep in insights:
                            with st.expander(f"📌 {rep.get('category', 'Unknown Category')}", expanded=True):
                                st.write(rep.get('analysis', 'No analysis found.'))
                    else:
                        st.info(str(insights))
                
                with col2:
                    st.header("🛡️ Ironclad Audit")
                    st.markdown("Automated hallucination scoring and fact verification.")
                    st.info(audit_output)

        except Exception as e:
            st.error(f"An error occurred during execution: {e}")
        finally:
            if os.path.exists(tmp_pdf_path):
                os.remove(tmp_pdf_path)
else:
    # Display splash / welcome area
    st.markdown("<br/><br/>", unsafe_allow_html=True)
    cols = st.columns(3)
    
    cols[0].info("**Document Parsing**\n\nAutomatically splits and embeds complex legal agreements into logical chunks.")
    cols[1].info("**Semantic Clustering**\n\nIdentifies hidden relationships and distinct legal topics using KMeans algorithm.")
    cols[2].info("**Ironclad Auditing**\n\nRuns a rigorous LLM extraction to fact-check the generated outputs back to the source text.")
    
    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #64748b;'>Awaiting user input. Please use the sidebar to connect your data.</p>", unsafe_allow_html=True)
