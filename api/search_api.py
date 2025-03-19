from fastapi import FastAPI, HTTPException
import faiss
import numpy as np
import json
from sentence_transformers import SentenceTransformer

app = FastAPI()

# Load FAISS index
index = faiss.read_index("jfk_index.faiss")

# Load metadata
with open("metadata.json", "r") as f:
    metadata = json.load(f)

# Load BGE-M3 model for queries
model = SentenceTransformer("BAAI/bge-m3")

@app.post("/search")
async def search_documents(query: str, top_k: int = 5):
    """Search for the most relevant documents."""
    try:
        # Convert query to embedding
        query_embedding = model.encode([query], convert_to_numpy=True)

        # Search FAISS index
        distances, indices = index.search(query_embedding, top_k)

        # Fetch matching documents
        results = [metadata[idx] for idx in indices[0] if idx != -1]

        return {"query": query, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
