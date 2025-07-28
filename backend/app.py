from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Query(BaseModel):
    question: str

@app.post("/ask")
def ask_question(query: Query):
    
    from rag_chain import query_rag  
    answer = query_rag(query.question)
    return {"answer": answer}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
