from fastapi import FastAPI, HTTPException
import faiss
import numpy as np
import json
from sentence_transformers import SentenceTransformer
from pydantic import BaseModel

app = FastAPI()

# Load FAISS index
index = faiss.read_index("./embeddings/jfk_index.faiss")

# Load metadata
with open("./embeddings/metadata.json", "r") as f:
    metadata = json.load(f)

# Load BGE-M3 model for queries
model = SentenceTransformer("BAAI/bge-m3")

# Define request model
class SearchQuery(BaseModel):
    query: str

@app.post("/search")
async def search_documents(search_query: SearchQuery, top_k: int = 5):
    """Search for the most relevant documents."""
    try:
        # Convert query to embedding
        query_embedding = model.encode([search_query.query], convert_to_numpy=True)

        # Search FAISS index
        distances, indices = index.search(query_embedding, top_k)

        # Fetch matching documents
        results = [metadata[idx] for idx in indices[0] if idx != -1]

        return {"query": search_query.query, "results": results}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
