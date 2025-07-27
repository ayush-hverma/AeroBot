import os
import faiss
import pickle
from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS
from langchain.docstore.document import Document

model = SentenceTransformer("all-MiniLM-L6-v2")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FAISS_PATH = os.path.join(BASE_DIR, "faiss_index", "index.faiss")
DOCS_PATH = os.path.join(BASE_DIR, "data", "documents.pkl")

def chunk_text(text, chunk_size=500, overlap=100):
    chunks = []
    start = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunks.append(text[start:end])
        start += chunk_size - overlap
    return chunks

def build_vector_store(texts):
    all_chunks = []
    for text in texts:
        chunks = chunk_text(text)
        all_chunks.extend(chunks)

    docs = [Document(page_content=chunk) for chunk in all_chunks]
    embeddings = model.encode([doc.page_content for doc in docs])

    index = faiss.IndexFlatL2(embeddings[0].shape[0])
    index.add(embeddings)

    faiss.write_index(index, FAISS_PATH)
    with open(DOCS_PATH, "wb") as f:
        pickle.dump(docs, f)

def load_vector_store():
    index = faiss.read_index(FAISS_PATH)
    with open(DOCS_PATH, "rb") as f:
        docs = pickle.load(f)
    return index, docs
