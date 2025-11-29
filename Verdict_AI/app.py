import streamlit as st
from modules.rag_engine import get_legal_analysis, ask_question
from PyPDF2 import PdfReader


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username == "harinie123" and password == "123":
            st.session_state.logged_in = True
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid username or password")
    st.stop()

# --- MAIN APP ---
st.set_page_config(page_title="Verdict AI", layout="wide")
st.title(" Verdict AI - Legal Document Analyzer and Q&A Bot")

st.markdown("###  Upload Legal Document (TXT or PDF)")

uploaded_file = st.file_uploader("Drop a file here", type=["txt", "pdf"])

# Load document content into session_state
if uploaded_file and "document_text" not in st.session_state:
    if uploaded_file.type == "text/plain":
        st.session_state.document_text = uploaded_file.read().decode("utf-8")
    elif uploaded_file.type == "application/pdf":
        reader = PdfReader(uploaded_file)
        st.session_state.document_text = "\n".join(
            [page.extract_text() for page in reader.pages if page.extract_text()]
        )

document_text = st.session_state.get("document_text", "")

if document_text:
    st.markdown("###  Preview of Document")
    st.text_area("Document Content", value=document_text[:3000], height=250)

    if st.button("Analyze Document") or "analysis_result" in st.session_state:
        if "analysis_result" not in st.session_state:
            with st.spinner("Analyzing..."):
                st.session_state.analysis_result = get_legal_analysis(document_text)

        st.success("Analysis Result:")
        st.write(st.session_state.analysis_result)

    st.markdown("---")
    st.markdown("###  Ask a Question")

    question = st.text_input("What would you like to know about this document?")

    if st.button("Ask"):
        if question.strip():
            with st.spinner("Thinking..."):
                answer = ask_question(document_text, question)
            st.success("Answer:")
            st.write(answer)
        else:
            st.warning("Please enter a question.")
