import os
import cohere
from dotenv import load_dotenv

load_dotenv()

co = cohere.Client(os.getenv("COHERE_API_KEY"))

def get_legal_analysis(text):
    try:
        response = co.chat(
            model="command-r-plus-08-2024",
            message=f"Analyze this legal document and provide insights:\n\n{text}",
            temperature=0.4,
        )
        return response.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"

def ask_question(document_text, question):
    try:
        chat_response = co.chat(
            model="command-r-plus-08-2024",
            message=f"""The following is a legal document:

{document_text}

Based on this, answer the question: {question}""",
            temperature=0.3
        )
        return chat_response.text.strip()
    except Exception as e:
        return f"Error: {str(e)}"
