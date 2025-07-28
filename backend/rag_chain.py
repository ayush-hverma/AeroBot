import google.generativeai as genai
from sentence_transformers import SentenceTransformer
import numpy as np
from dotenv import load_dotenv
import os

from langchain.docstore.document import Document
from vectorstore import load_vector_store

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Global cache (None initially)
model = None
embedder = None
index = None
documents = None

def query_rag(question):
    global model, embedder, index, documents

    if model is None:
        model = genai.GenerativeModel("gemini-2.5-flash")
    
    if embedder is None:
        embedder = SentenceTransformer("all-MiniLM-L6-v2")
    
    if index is None or documents is None:
        index, documents = load_vector_store()

    query_embedding = embedder.encode([question])[0]
    D, I = index.search(np.array([query_embedding]), k=5)
    retrieved_docs = [documents[i].page_content for i in I[0]]
    context = "\n\n".join(retrieved_docs)

    prompt = f"""Use the following information to answer the question:\n{context}\n\nQuestion: {question}"""
    response = model.generate_content(prompt)
    return response.text
