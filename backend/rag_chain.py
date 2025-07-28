import google.generativeai as genai
from sentence_transformers import SentenceTransformer
import numpy as np
from langchain.docstore.document import Document
from vectorstore import load_vector_store
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

index, documents = load_vector_store()

def query_rag(question):
    query_embedding = embedder.encode([question])[0]
    D, I = index.search(np.array([query_embedding]), k=5)
    retrieved_docs = [documents[i].page_content for i in I[0]]
    context = "\n\n".join(retrieved_docs)
    prompt = f"""Use the following information to answer the question:\n{context}\n\nQuestion: {question}"""
    response = model.generate_content(prompt)
    return response.text
